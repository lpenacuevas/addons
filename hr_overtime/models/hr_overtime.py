from odoo import models, fields, api
from datetime import datetime, timedelta
from calendar import monthrange
import logging

_logger = logging.getLogger(__name__)


class overtime_users(models.Model):
    _name = 'hr.overtime'
    _description = 'Labor extraordinaria'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado(a)',
    )

    job_id = fields.Many2one('hr.job', string='Cargo')
    departament_id = fields.Many2one('hr.department', string='Deparmento')
    standard_hours = fields.Many2one('resource.calendar', string='Horas estandar')
    total_hours = fields.Float(string='Horas totales')
    extra_hours = fields.Float(string='Horas extras')
    salary = fields.Char(string='Salario', )
    date_start = fields.Date(string="Fecha de inicio", default=datetime.today().replace(day=1))
    date_end = fields.Date(string="Fecha final", default=lambda self: self._default_last())
    periodo = fields.Char(string=f"{date_start} hasta {date_end}")

    @api.model
    def _default_last(self):
        # Retorna el último día del mes actual
        today = datetime.now()
        ultimo_dia = monthrange(today.year, today.month)[1]
        return today.replace(day=ultimo_dia)

    @api.onchange('employee_id', 'date_end')
    def _get_fields(self):
        for record in self:
            employee_obj = self.env['hr.attendance'].search(
                [('employee_id', '=', record.employee_id.id)], limit=1)
            if record.employee_id and record.date_end:
                record.job_id = record.employee_id.job_id.id
                record.departament_id = record.employee_id.department_id.id
                record.salary = record.employee_id.salary
                record.standard_hours = record.employee_id.resource_calendar_id
                record.total_hours = employee_obj.worked_hours
                if not employee_obj:
                    record.extra_hours = 0.00
                else:
                    record.extra_hours = record.total_hours - record.standard_hours.time_per_week
