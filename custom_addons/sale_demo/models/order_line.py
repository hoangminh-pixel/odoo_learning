from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _name = 'sale.demo.order.line'
    _description = 'Sale Order Line'

    order_id = fields.Many2one(
        'sale.demo.order',
        string='Order',
        ondelete='cascade'
    )

    product_name = fields.Char(string='Product')
    quantity = fields.Integer(string='Quantity', default=1)
    price = fields.Float(string='Price')

    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True
    )

    @api.depends('quantity', 'price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price