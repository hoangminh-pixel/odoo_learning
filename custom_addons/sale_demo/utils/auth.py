from functools import wraps
from odoo.http import request
import jwt
from .jwt_helper import decode_token
from ..utils.response import error


def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.httprequest.headers.get('Authorization')

        if not auth or not auth.startswith('Bearer '):
            return error(401, 'Missing token', 401)

        try:
            token = auth.split(' ')[1]
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            return error(401, 'Token expired', 401)
        except Exception:
            return error(401, 'Invalid token', 401)

        if payload.get('type') != 'access_token':
            return error(401, 'Invalid token type', 401)

        user = request.env['res.users'].sudo().browse(payload['uid'])
        if not user.exists():
            return error(401, 'User not found', 401)

        # request.api_user = user

        return func(*args, **kwargs)

    return wrapper
