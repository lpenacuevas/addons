from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def open_wizard_planning(self):
        vacation_from_plan = self.env['hr.vacation.plan'].search([('employee_id', '=', self.id)]).mapped('date')
        min_year = min(vacation_from_plan).year
        return {
            'name': 'Planificacion de Vacaciones',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.vacation.wizard',
            'view_mode': "form",
            'target': 'new',
            'context': {
                'default_employee_id': self.id,
                'default_department_id': self.department_id.id,
                'default_job_id': self.job_id.id,
                'default_coach_id': self.coach_id.id,
                'default_year_vacation': min_year
            }
        }
