from odoo import models, fields

class TestmModel(models.Model):
    _name = 'test.model'
    _description = 'Test Model'

    name = fields.Char(string='Test Name', required=True)
    description = fields.Text()
    start_date = fields.Date()
    end_date = fields.Date()
    active = fields.Boolean(default=True)