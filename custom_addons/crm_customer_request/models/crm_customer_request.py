from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CrmCustomerRequest(models.Model):
    _name = 'crm.customer.request'
    _description = 'Customer Request'

    product_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True
    )

    opportunity_id = fields.Many2one(
        'crm.lead',
        string='Opportunity',
        required=True,
        ondelete='cascade'
    )

    date = fields.Date(
        default=fields.Date.today,
        required=True
    )

    description = fields.Text()

    qty = fields.Float(
        default=1,
        required=True
    )

