from odoo import http
from odoo.http import request, Response
import json
from ..utils.response import success, error


class SaleDemoAPI(http.Controller):

    @http.route('/api/ping', type='http', auth='public')
    def ping(self):
        return "pong"

    @http.route('/api/test', type='json', auth='public', methods=['POST'], csrf=False)
    def test(self):
        return {'ok': True}

    # -------- CREATE --------

    @http.route(
        '/api/orders/create',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def create_order(self):
        payload = request.get_json_data()
        order = request.env['sale.demo.order'].sudo().api_create(payload)
        return success(order, status=200)

    # -------- READ LIST --------
    @http.route('/api/orders', type='http', auth='public', csrf=False, methods=['GET'])
    def get_orders(self):
        return success(request.env['sale.demo.order'].sudo().api_get_list(), status=200)

    # -------- READ DETAIL --------
    @http.route('/api/orders/detail', type='http', auth='public', csrf=False)
    def get_order_detail(self):
        payload = request.get_json_data()
        id = payload.get('id')
        order = request.env['sale.demo.order'].sudo().browse(id)
        if not order.exists():
            return error(code=404, message='Order not found', status=404)
        return success(order.api_read_detail(), status=200)

    # -------- UPDATE --------
    @http.route('/api/orders/update', type='http', auth='public', csrf=False)
    def update_order(self):
        payload = request.get_json_data()
        id = payload.get('id')
        order = request.env['sale.demo.order'].sudo().browse(id)
        if not order.exists():
            return error(code=404, message='Order not found', status=404)
        return success(order.api_update(payload), status=200)

    # -------- DELETE --------
    @http.route('/api/orders/delete', type='http', auth='public', csrf=False)
    def delete_order(self):
        payload = request.get_json_data()
        id = payload.get('id')
        order = request.env['sale.demo.order'].sudo().browse(id)
        if not order.exists():
            return error(code=404, message='Order not found', status=404)
        return success(order.api_delete(), status=200)

    @http.route(
        '/api/orders/delete_all',
        type='http',
        auth='public',
        csrf=False,
        methods=['POST']
    )
    def delete_all_orders(self):
        order = request.env['sale.demo.order'].sudo().api_delete_all()
        return success(order, status=200)
