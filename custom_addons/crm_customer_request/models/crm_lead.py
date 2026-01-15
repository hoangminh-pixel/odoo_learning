from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    request_ids = fields.One2many(
        'crm.customer.request',
        'opportunity_id',
        string='Customer Requests'
    )

    total_qty = fields.Float(
        string='Total Quantity',
        compute='_compute_request_summary',
        store=True
    )

    expected_revenue_from_request = fields.Float(
        string='Expected Revenue (Request)',
        compute='_compute_request_summary',
        store=True
    )

    is_new_stage = fields.Boolean(
        compute='_compute_is_new_stage',
        store=True
    )

    @api.depends('stage_id')
    def _compute_is_new_stage(self):
        for rec in self:
            rec.is_new_stage = rec.stage_id.sequence == 1

    @api.depends(
        'request_ids.qty',
        'request_ids.product_id.list_price'
    )
    def _compute_request_summary(self):
        for lead in self:
            total_qty = 0
            total_amount = 0
            for req in lead.request_ids:
                total_qty += req.qty
                total_amount += req.qty * req.product_id.list_price

            lead.total_qty = total_qty
            lead.expected_revenue_from_request = total_amount
