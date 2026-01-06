from odoo import models, fields

class MyModel(models.Model):
      _name = 'my.model'

      name = fields.Char()
      description = fields.Text()
      duration = fields.Integer()