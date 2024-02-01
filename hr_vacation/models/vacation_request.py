from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class VacationRequest(models.Model):
    _name = 'vacation.request'

    date_from = fields.Date('Desde')
    date_to = fields.Date('Hasta', readonly=True)
    date_return = fields.Date('Fecha de retorno', readonly=True)

    vacation_time = fields.Integer('Cantidad de dias', readonly=True)

    employee_id = fields.Many2one('hr.employee', 'Empleado', readonly=True)

    department_id = fields.Many2one('hr.department', 'Departamento', readonly=True)
    job_id = fields.Many2one('hr.job', 'Puesto de trabajo', readonly=True)
    coach_id = fields.Many2one('hr.employee', 'Supervisor Inmediato', readonly=True)
    year_vacation = fields.Integer(string='Periodo', help="Año al cual corresponden dichas vacaciones", readonly=True)

    state = fields.Selection(related="stage_id.state", string='Estado', readonly=False)

    stage_id = fields.Many2one("hr.vacation.stage")

    identifier = fields.Integer("Identificador de planificacion", readonly=True)

    is_created = fields.Boolean()

    def action_confirm(self):
        for rec in self:
            stage_approved = rec.env["hr.vacation.stage"].search([("state", "=", "approved")]).id
            rec.write({'stage_id': stage_approved})
            rec.env['hr.vacation.planning'].search([('id', '=', rec.identifier)]).write({'stage_id': stage_approved})
            # leave_type = rec.env['hr.leave.type'].search([('type_vacation', '=', 'vacation')])
            # if leave_type:
            #     rec.env['hr.leave'].create({
            #         'holiday_status_id': leave_type.id,
            #         'holiday_type': 'employee',
            #         'employee_ids': [(6, 0, [rec.employee_id.id])],
            #         'request_date_from': rec.date_from,
            #         'request_date_to':   rec.date_to,
            #         'number_of_days': float(rec.vacation_time),
            #         'state': 'validate',
            #     })
            # else:
            #     raise ValidationError('La ausencia tipo vacaciones aún no ha sido creada.')

    def action_refuse(self):
        for rec in self:
            stage_cancel = rec.env["hr.vacation.stage"].search([("state", "=", "cancel")]).id
            rec.write({'stage_id': stage_cancel})
            rec.env['hr.vacation.planning'].search([('id', '=', rec.identifier)]).write({'stage_id': stage_cancel})

    def create_staff_from_request(self):
        for rec in self:
            if rec.state == 'approved':
                vacation_from_plan = rec.env['hr.vacation.plan'].search([('employee_id', '=', rec.employee_id.id)])
                holiday_period = min(
                    rec.env['hr.vacation.plan'].search([('employee_id', '=', rec.employee_id.id)]).mapped('date'))
                oldest_vacation = vacation_from_plan.sorted(key=lambda r: r.date)[0]
                if oldest_vacation:
                    if oldest_vacation.taken != 0:
                        oldest_vacation.taken = oldest_vacation.taken - rec.vacation_time
                    else:
                        oldest_vacation.taken = rec.vacation_time
                action_type_lower = rec.env['action.type'].search([('name', '=', 'DISFRUTE DE VACACIONES')])
                if action_type_lower:
                    action_type_lower.name.lower()
                else:
                    raise ValidationError('La accion de tipo "DISFRUTE DE VACACIONES" aún no ha sido creada')
                if rec.is_created:
                    raise ValidationError('La novedad ya ha sido creada anteriormente')
                return {
                    'name': 'Novedades',
                    'type': 'ir.actions.act_window',
                    'res_model': 'staff.planning.wizard',
                    'view_mode': "form",
                    'target': 'new',
                    'context': {
                        'default_action_type_id': action_type_lower.id,
                        'default_employee_id': rec.employee_id.id,
                        'default_departments_id': rec.department_id.id,
                        'default_position_id': rec.job_id.id,
                        'default_salary': rec.employee_id.salary,
                        'default_action_motivation': f'Vacaciones desde {rec.date_from} hasta {rec.date_to}, tomando {rec.vacation_time} días correspondientes a las vacaciones del periodo {holiday_period.year}, le quedan {oldest_vacation.available} días.',
                    }
                }
            else:
                raise UserError(
                    'La solicitud necesita ser aprovada antes de ser creada la novedad. Por favor, verifique el estado de la planificación.')
