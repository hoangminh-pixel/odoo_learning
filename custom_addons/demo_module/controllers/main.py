from odoo import http
from odoo.http import request

class TrainingDemoController(http.Controller):

    @http.route('/training/demo', auth='public', website=True)
    def demo_page(self):
        courses = request.env['training.course'].sudo().search([])
        return "<br/>".join(courses.mapped('name'))
