from odoo import http
from odoo.exceptions import AccessDenied, ValidationError
from odoo.http import request
from ..utils.response import success, error
from ..utils.auth import require_auth


class SaleDemoAPI(http.Controller):

    # @http.route('/api/ping', type='http', auth='public')
    # def ping(self):
    #     return "pong"

    # @http.route('/api/test', type='json', auth='public', methods=['POST'], csrf=False)
    # def test(self):
    #     return {'ok': True}

    # -------- CREATE --------
    @http.route(
        '/api/orders/create',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    @require_auth
    def create_order(self):
        try:
            payload = request.get_json_data()
            order = request.env['sale.demo.order'].sudo().api_create(payload)
            return success(order, status=200)
        except ValidationError as e:
            return error(code=400, message=str(e), status=400)

        except Exception as e:
            return error(code=400, message=str(e), status=400)

    # -------- READ LIST --------
    @http.route('/api/orders', type='http', auth='public', csrf=False, methods=['GET'])
    @require_auth
    def get_orders(self):
        try:
            params = request.httprequest.args

            limit = params.get('limit', 20)
            page = params.get('page', 1)

            result = request.env['sale.demo.order'].sudo().api_get_list(
                limit=limit,
                page=page
            )
            return success(result, status=200)
        except AccessDenied as e:
            return error(code=403, message=str(e), status=403)
        except Exception as e:
            return error(code=400, message=str(e), status=400)

    # -------- READ DETAIL --------
    @http.route('/api/orders/detail', type='http', auth='public', csrf=False)
    @require_auth
    def get_order_detail(self):
        try:
            payload = request.get_json_data()
            id = payload.get('id')
            order = request.env['sale.demo.order'].sudo().browse(id)
            if not order.exists():
                return error(code=404, message='Order not found', status=404)
            return success(order.api_read_detail(), status=200)
        except Exception as e:
            return error(code=400, message=str(e), status=400)

    # -------- UPDATE --------
    @http.route('/api/orders/update', type='http', auth='public', csrf=False)
    @require_auth
    def update_order(self):
        try:
            payload = request.get_json_data()
            id = payload.get('id')
            order = request.env['sale.demo.order'].sudo().browse(id)
            if not order.exists():
                return error(code=404, message='Order not found', status=404)
            return success(order.api_update(payload), status=200)
        except Exception as e:
            return error(code=400, message=str(e), status=400)

    # -------- DELETE --------
    @http.route('/api/orders/delete', type='http', auth='public', csrf=False)
    @require_auth
    def delete_order(self):
        try:
            payload = request.get_json_data()
            id = payload.get('id')
            order = request.env['sale.demo.order'].sudo().browse(id)
            if not order.exists():
                return error(code=404, message='Order not found', status=404)
            return success(order.api_delete(), status=200)
        except Exception as e:
            return error(code=400, message=str(e), status=400)

    @http.route(
        '/api/orders/delete_all',
        type='http',
        auth='public',
        csrf=False,
        methods=['POST']
    )
    @require_auth
    def delete_all_orders(self):
        try:
            order = request.env['sale.demo.order'].sudo().api_delete_all()
            return success(order, status=200)
        except Exception as e:
            return error(code=400, message=str(e), status=400)
