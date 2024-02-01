import logging
from odoo import models, fields, api
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class custom_hr_employee(models.Model):
    _inherit = "hr.employee"
    #     _description = 'departamento_localidad.departamento_localidad'

    tipo_condicion = fields.Many2one(
        "condition.types",
        string='Tipo de condicion',
        required=True
    )

    last_name = fields.Char()

    tipo_empleado = fields.Many2one(
        "employee.types",
        string="Tipo de empleado",
        required=True
    )

    enter_date = fields.Date(
        string='Fecha de Ingreso', required=True)
    end_date = fields.Date(
        string='Fecha de Egreso')

    other_institution_month = fields.Integer(
        string='Mes',
        required=False,
        domain="[('other_institution_month', '>=', 0), ('other_institution_month', '<=', 12)]")
    other_institution_year = fields.Integer(
        string='Año',
        required=False)

    department_id = fields.Many2one(
        'hr.department',
        string='Departamento')

    years_passed = fields.Integer(string='Years Passed', compute='_compute_years_months')
    months_passed = fields.Integer(string='Months Passed', compute='_compute_years_months')

    government_time_years = fields.Integer(string='Años totales', readonly=True)
    government_time_months = fields.Integer(string='Meses totales', readonly=True)
    id_mrh = fields.Integer()

    salary = fields.Float('Salario')

    @api.depends('enter_date', 'end_date')
    def _compute_years_months(self):
        for rec in self:
            if rec.enter_date:
                if not rec.end_date:
                    stored_date = rec.enter_date
                    current_date = datetime.now().date()
                    difference = current_date - stored_date
                    rec.years_passed = difference.days // 365
                    rec.months_passed = (difference.days % 365) // 30
                elif rec.end_date:
                    difference = rec.end_date - rec.enter_date
                    rec.years_passed = difference.days // 365
                    rec.months_passed = (difference.days % 365) // 30
            else:
                rec.years_passed = 0
                rec.months_passed = 0

    def name_get(self):
        result = []
        for rec in self:
            name = f"{rec.name} {rec.last_name}"
            result.append((rec.id, name))
        return result

    @api.onchange('enter_date', 'end_date', 'other_institution_year', 'other_institution_month')
    def _compute_government_time_total(self):
        for rec in self:
            total_years = rec.years_passed + rec.other_institution_year
            total_months = rec.months_passed + rec.other_institution_month
            additional_years = total_months // 12
            total_years += additional_years
            rec.government_time_years = total_years
            rec.government_time_months = total_months % 12

    @api.onchange('enter_date')
    def get_vacation_plan(self):
        for rec in self:
            if rec.enter_date:
                available_days = 0
                if 1 <= rec.government_time_years <= 5:
                    available_days = 15
                elif 5 < rec.government_time_years <= 10:
                    available_days = 20
                elif 10 < rec.government_time_years <= 15:
                    available_days = 25
                else:
                    available_days = 30
                next_year = rec.enter_date.year + 1
                next_date = rec.enter_date.replace(year=next_year)
                if datetime.now().date() == next_date:
                    rec.env['hr.vacation.plan'].create({
                        'date': next_date,
                        'employee_id': str(rec.id).split('_')[-1],
                        'taken': 0,
                        'available': available_days
                    })

    @api.constrains('departure_date')
    def _get_end_date(self):
        for rec in self:
            if not rec.active:
                rec.end_date = rec.departure_date
