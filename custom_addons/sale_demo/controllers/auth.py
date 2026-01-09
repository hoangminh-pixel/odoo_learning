from odoo import http
from odoo.exceptions import AccessDenied
from odoo.http import request, Response
import json
from ..utils.jwt_helper import (
    create_access_token,
    create_refresh_token,
    decode_token
)
from ..utils.response import success, error


class AuthController(http.Controller):

    @http.route('/api/test/auth', type='http', auth='public', csrf=False, methods=['POST'])
    def test(self):

        return success({
            'ok': True,
        }, status=200)

    @http.route('/api/auth/login', type='http', auth='public', csrf=False, methods=['POST'])
    def login(self):
        try:
            data = request.get_json_data()
            login = data.get('login')
            password = data.get('password')

            if not login or not password:
                return error(code=400, message='Missing login or password', status=400)

            uid = request.session.authenticate(
                request.db,
                login,
                password
            )

            if not uid:
                return error(401, 'Invalid credentials', 401)

            user = request.env['res.users'].sudo().browse(uid)

            if not user:
                return error(code=401, message='Invalid credentials', status=401)

            try:
                user._check_credentials(password, request.httprequest.environ)
            except AccessDenied:
                return error(401, 'Access Denied', 401)

            return success({
                'access_token': create_access_token(user),
                'refresh_token': create_refresh_token(user),
                'user': {
                    'id': user.id,
                    'login': user.login,
                    'name': user.name,
                }
            }, status=200)
        except Exception as e:
            return error(code=400, message=str(e), status=400)

    @http.route('/api/auth/refresh', type='http', auth='public', csrf=False, methods=['POST'])
    def refresh(self):
        try:
            data = request.get_json_data()
            token = data.get('refresh_token')
            payload = decode_token(token)
            if payload.get('type') != 'refresh_token':
                return error(401, 'Invalid token', 401)
            user = request.env['res.users'].sudo().browse(payload['uid'])
            return success({
                'access_token': create_access_token(user)
            }, status=200)
        except Exception as e:
            return error(code=400, message=str(e), status=400)
