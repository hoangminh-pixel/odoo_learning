from odoo import models, fields

class Student(models.Model):
      _name = 'training.student'
      student_name = fields.Char()
      age = fields.Integer()
      email = fields.Char()
      is_study = fields.Boolean() 