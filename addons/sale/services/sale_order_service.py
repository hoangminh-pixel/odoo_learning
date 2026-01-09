from odoo import fields
from odoo.http import request


class SaleOrderService:

    @staticmethod
    def get_list(payload):

        env = request.env['sale.order'].sudo()
        date_from = payload.get('date_from') or fields.Date.today()
        date_to = payload.get('date_to') or fields.Date.today()

        domain = [
            ('create_date', '>=', date_from),
            ('create_date', '<=', date_to),
        ]

        orders = env.search(domain)
        total = len(orders)
        amount_total = 0

        data = []
        for order in orders:
            order_lines = []
            for line in order.order_line:
                line_total = line.price_unit * line.product_uom_qty
                amount_total += line_total

                order_lines.append({
                    'id': line.id,
                    'product_name': line.name,
                    'quantity': line.product_uom_qty,
                    'price': line.price_unit,
                    'subtotal': line_total,
                })

            data.append({
                'id': order.id,
                'name': order.name,
                'create_date': order.create_date.isoformat() if order.create_date else None,
                'state': order.state,
                'line_ids': order_lines
            })

        return {
            'success': True,
            'data': {
                'product_total': total,
                'amount_total': amount_total,
                'data': data,
            }}
