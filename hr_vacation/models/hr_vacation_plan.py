from odoo import api, fields, models


class HrVacationPlan(models.Model):
    _name = 'hr.vacation.plan'
    _description = 'HrVacacionPlan'

    date = fields.Date('Fecha')
    employee_id = fields.Many2one('hr.employee', 'Empleados')
    available = fields.Integer('Disponibles')
    taken = fields.Integer('Tomados')

    @api.constrains('taken')
    def _get_available_days(self):
        for rec in self:
            if rec.taken:
                rec.available = rec.available - rec.taken
