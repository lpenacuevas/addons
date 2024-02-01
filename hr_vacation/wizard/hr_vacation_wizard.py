from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta, datetime
import logging

_logger = logging.getLogger(__name__)


class HrVacationWizard(models.TransientModel):
    _name = 'hr.vacation.wizard'

    date_from = fields.Date('Desde')
    date_to = fields.Date('Hasta')
    date_return = fields.Date('Fecha de retorno')

    time_spent = fields.Integer('Cantidad de dias')
    vacation_time = fields.Integer()

    employee_id = fields.Many2one('hr.employee', 'Empleado')

    department_id = fields.Many2one('hr.department', 'Departamento')
    job_id = fields.Many2one('hr.job', 'Puesto de trabajo')
    coach_id = fields.Many2one('hr.employee', 'Supervisor Inmediato')

    state = fields.Selection(related="stage_id.state", string='Estado')
    year_vacation = fields.Integer(string='Periodo', help="Año al cual corresponden dichas vacaciones")

    stage_id = fields.Many2one(
        "hr.vacation.stage",
        default=lambda self: self.env["hr.vacation.stage"].search([("state", "=", "to approved")],
                                                                  limit=1),
        group_expand="_group_expand_stage_id",
    )

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)

    ###METHOD TO COMPUTE VACATION DAYS WITHOUT HOLIDAYS###

    @api.onchange('date_from', 'date_to')
    def _compute_time_spent_from_dates(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                if rec.date_from > rec.date_to:
                    raise UserError('La fecha final debe ser mayor o igual a la fecha inicial')
                holidays = self.env['hr.vacation.holiday'].search([]).mapped('date')
                working_dates = []
                current_date = rec.date_from
                while current_date <= rec.date_to:
                    if current_date.weekday() < 5 and current_date not in holidays:
                        working_dates.append(current_date)
                    current_date += timedelta(days=1)
                rec.time_spent = len(working_dates)
                next_day = rec.date_to + timedelta(days=1)
                if next_day.weekday() < 5 and next_day not in holidays:
                    rec.date_return = next_day
                elif next_day.weekday() >= 5 and next_day not in holidays:
                    rec.date_return = next_day + timedelta(days=2)




    def save_vacation_planning(self):
        for rec in self:
            rec.vacation_time = rec.time_spent
            rec.env['hr.vacation.planning'].create({
                'employee_id': rec.employee_id.id,
                'department_id': rec.department_id.id,
                'job_id': rec.job_id.id,
                'coach_id': rec.coach_id.id,
                'date_from': rec.date_from,
                'date_to': rec.date_to,
                'vacation_time': rec.vacation_time,
                'date_return': rec.date_return,
                'year_vacation': rec.year_vacation,
                'state': rec.state,
                'stage_id': rec.stage_id.id,
            })


