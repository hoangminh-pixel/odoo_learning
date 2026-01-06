from odoo import models, fields

class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'Training Course'

    name = fields.Char(string='Course Name', required=True)
    description = fields.Text()
    start_date = fields.Date()
    end_date = fields.Date()
    active = fields.Boolean(default=True)
