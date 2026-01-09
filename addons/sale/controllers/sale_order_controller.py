import json
from odoo import http
from odoo.exceptions import AccessDenied, ValidationError
from odoo.http import Response, request
from ..services.sale_order_service import SaleOrderService


class SaleController(http.Controller):
    @http.route('/sale/ping', type='http', auth='public', csrf=False)
    def ping(self):
        return "ping"

    @http.route('/sales/list', type='http', auth='public', csrf=False)
    def get_list(self):
        payload = request.get_json_data()

        try:
            res = SaleOrderService.get_list(payload)
            return Response(
                json.dumps(res, default=str),
                status=200,
                mimetype='application/json'
            )

        except Exception as e:
            return Response(
                json.dumps(e, default=str),
                status=400,
                mimetype='application/json'
            )
