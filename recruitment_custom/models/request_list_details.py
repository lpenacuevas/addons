from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class RequestListDetails(models.Model):
    _name = 'request.list.details'
    _order = 'duration ASC'

    job_id = fields.Many2one('hr.job', string='Job')

    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    department_id = fields.Many2one('hr.department', string='Departmento', readonly=True)

    details = fields.Char(string='Detalle')

    date_from = fields.Date(string='Fecha desde', default=fields.Date.today, required=True)
    date_to = fields.Date(string='Fecha hasta', required=True)

    remaining_days = fields.Char(string='Duración')
    duration = fields.Integer()

    @api.onchange('date_from', 'date_to')
    def _compute_duration(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                remaining = rec.date_to - rec.date_from
                rec.duration = remaining.days
                if rec.duration != 0:
                    rec.remaining_days = f"{remaining.days} días"
                else:
                    rec.remaining_days = 'Expirada'


    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for rec in self:
            if rec.employee_id:
                rec.department_id = rec.employee_id.department_id.id

    # def send_mail_notification(self):
    #     for rec in self:
    #         get_email_to = rec.env['hr.employee'].search([('employee_id', '=')])
    #         mail = rec.env['mail.mail'].create({
    #             'model': rec._name,
    #             'res_id': rec.id,
    #             'subject': "",
    #             'body_html': "",
    #             'email_from': rec.env.user.email,
    #             'email_to': ,
    #         })
    #         mail.send()
