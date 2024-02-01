from datetime import timedelta, datetime
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class HrVacationPlanning(models.Model):
    _name = 'hr.vacation.planning'
    _inherit = ['mail.thread']

    date_from = fields.Date('Desde')
    date_to = fields.Date('Hasta')
    date_return = fields.Date('Fecha de retorno')

    vacation_time = fields.Integer('Cantidad de dias')

    employee_id = fields.Many2one('hr.employee', 'Empleado')

    department_id = fields.Many2one('hr.department', 'Departamento')
    job_id = fields.Many2one('hr.job', 'Puesto de trabajo')
    coach_id = fields.Many2one('hr.employee', 'Supervisor Inmediato')
    year_vacation = fields.Integer(string='Periodo', help="Año al cual corresponden dichas vacaciones")

    is_requested = fields.Boolean(default=False)

    state = fields.Selection(related="stage_id.state", string='Estado')

    stage_id = fields.Many2one("hr.vacation.stage")

    def create_vacation_request(self):
        for rec in self:
            if rec.state == "to approved":
                if rec.is_requested:
                    raise UserError(
                        'No es posible crear la solicitud, debido a que esta ya ha sido creada anteriormente')
                rec.env['vacation.request'].create({
                    'date_from': rec.date_from,
                    'date_to': rec.date_to,
                    'date_return': rec.date_return,
                    'vacation_time': rec.vacation_time,
                    'employee_id': rec.employee_id.id,
                    'department_id': rec.department_id.id,
                    'job_id': rec.job_id.id,
                    'coach_id': rec.coach_id.id,
                    'year_vacation': rec.year_vacation,
                    'state': rec.state,
                    'stage_id': rec.stage_id.id,
                    'identifier': rec.id
                })
                rec.is_requested = True
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': ('Solicitud Realizada!'),
                        'message': 'Usted ha generado la petición satisfractoriamente',
                        'type': 'success',
                        'sticky': False,
                    },
                }
            else:
                raise UserError("Esta planificación se encuentra en proceso de aprobación")

    def send_notification_before_vacation(self):
        """This method trigger when there are 15 days remaining before vacation start"""
        for rec in self:
            if rec.date_from:
                if datetime.today() == rec.date_from.date() - timedelta(days=15):
                    if rec.employee_id.user_id and rec.coach_id.user_id:
                        rec.send_internal_notification()
                    else:
                        rec.send_email_notification()

    def send_notification_after_vacation(self):
        """This method trigger when there are no days remaining before returning to work"""
        for rec in self:
            if rec.date_return:
                if datetime.today() == rec.date_from.date():
                    rec.send_email_notification()

    def send_internal_notification(self):
        mod_responses = []
        for rec in self:
            mod_response = rec.env['mail.channel'].browse(rec.env.ref('base.partner_root').id).message_post(
                body=f'Solicitud de vacaciones pendientes para empleado {rec.employee_id.name} {rec.employee_id.last_name}',
                subject='Solicitud de vacaciones',
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
                author_id=rec.env.ref('base.partner_root').id
            )
            mod_responses.append(mod_response)
        return mod_responses

    def send_email_notification(self, body_html):
        receivers = [self.employee_id.work_email, self.coach_id.work_email]
        author_id = self.env.ref('base.partner_root').id
        email_from = self.env.ref('base.partner_root').email
        mail_values = {
            'subject': 'Solicitud de vacaciones',
            'body_html': body_html,
            'email_to': ','.join(receivers),
            'author_id': author_id,
            'email_from': email_from,
            'model': 'hr.vacation.planning',
            'res_id': self.id,
            'reply_to': 'noreply@example.com'
        }
        self.env['mail.mail'].create(mail_values).send()
