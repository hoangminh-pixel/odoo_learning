from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _name = 'sale.demo.order'
    _description = 'Sale Order Demo'

    name = fields.Char(string='Order Name', required=True)
    date_order = fields.Date(default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done')
    ], default='draft')

    partner_id = fields.Many2one('res.partner', string='Customer')
    line_ids = fields.One2many(
        'sale.demo.order.line',
        'order_id',
        string='Order Lines'
    )

    def action_open_detail(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order Detail',
            'res_model': 'sale.demo.order',
            'view_mode': 'form',
            'view_id': self.env.ref('sale_demo.view_order_form').id,
            'res_id': self.id,
            'target': 'current',
        }

    # ---------- CREATE ----------
    @api.model
    def api_create(self, vals):
        if not vals.get('name'):
            raise ValidationError("name is required")

        lines = vals.pop('line_ids', [])

        order = self.create({
            **vals,
            'line_ids': [
                (0, 0, {
                    'product_name': line['product_name'],
                    'quantity': line['quantity'],
                    'price': line['price'],
                })
                for line in lines
            ]
        })

        return order.api_read_detail()

    # ---------- READ LIST ----------
    @api.model
    def api_get_list(self, limit=20, page=1):
        limit = max(1, int(limit))
        page = max(1, int(page))
        offset = (page - 1) * limit


        orders = self.search([], limit=limit,
                             offset=offset, order='id desc')
        total = self.search_count([])

        return {
            'data': [o.api_read_detail() for o in orders],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'total_pages': (total + limit - 1) // limit
            }
        }
    # ---------- READ DETAIL ----------

    def api_read_detail(self):
        self.ensure_one()
        return {
            'id': self.id,
            'name': self.name,
            'partner_id': self.partner_id.id,
            'partner_name': self.partner_id.name,
            'date_order': self.date_order.isoformat() if self.date_order else None,
            'state': self.state,
            'line_ids': [
                {
                    'id': line.id,
                    # 'product_id': line.product_id.id,
                    'product_name': line.product_name,
                    'quantity': line.quantity,
                    'price': line.price,
                }
                for line in self.line_ids
            ]
        }

    # ---------- UPDATE ----------
    def api_update(self, vals):
        self.ensure_one()

        if 'line_ids' in vals:
            lines = vals.pop('line_ids')
            commands = []

            for l in lines:
                if l.get('id'):
                    commands.append((
                        1, l['id'], {   # UPDATE
                            'product_name': l['product_name'],
                            'quantity': l['quantity'],
                            'price': l['price'],
                        }
                    ))
                else:
                    commands.append((
                        0, 0, {         # CREATE
                            'product_name': l['product_name'],
                            'quantity': l['quantity'],
                            'price': l['price'],
                        }
                    ))

            vals['line_ids'] = commands

        self.write(vals)
        return self.api_read_detail()

    # ---------- DELETE ----------
    def api_delete(self):
        self.ensure_one()
        self.unlink()
        return {'message': 'Detele successfully!'}

    # ---------- DELETE ALL ----------
    @api.model
    def api_delete_all(self):
        orders = self.search([])
        count = len(orders)

        if not orders:
            return {
                'success': True,
                'deleted': 0,
                'message': 'No orders to delete'
            }

        orders.unlink()

        return {
            'success': True,
            'deleted': count,
            'message': 'All orders deleted'
        }
