import logging
from odoo import models, fields, api
from datetime import datetime

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

    years_passed = fields.Integer(string='Years Passed', compute='_compute_years_months', store=True)
    months_passed = fields.Integer(string='Months Passed', compute='_compute_years_months', store=True)

    government_years_total = fields.Integer(string='Years total', compute='_compute_government_time_total', store=True)
    government_months_total = fields.Integer(string='Months total', compute='_compute_government_time_total',
                                             store=True)
    id_mrh = fields.Integer()

    salary = fields.Float('Salario')

    @api.depends('enter_date')
    def _compute_years_months(self):
        for rec in self:
            if rec.enter_date:
                stored_date = rec.enter_date
                current_date = datetime.now().date()
                difference = current_date - stored_date
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

    @api.depends('enter_date')
    def _compute_government_time_total(self):
        for rec in self:
            if rec.other_institution_year:
                rec.government_years_total = rec.other_institution_year + rec.years_passed
                rec.government_months_total = rec.other_institution_month + rec.months_passed
