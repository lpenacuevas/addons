from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    employee_id = fields.Many2one('hr.employee', 'Empleado Relacionado')
