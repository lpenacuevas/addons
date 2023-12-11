import datetime
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class almuerzo_comida(models.Model):
    _name = 'almuerzo.despacho.almuerzo'
    _description = 'Modelo de registro de almuerzo diario'
    
    cedula = fields.Char("Cedula")
    first_name = fields.Char("Nombre")
    last_name = fields.Char("Apellidos")
    name = fields.Char("Nombre completo", store=True, compute="_compute_rec_name")
    unit = fields.Char("Unidad")
    employee_object = fields.Many2one("hr.employee")
    contact_object = fields.Many2one("res.partner")
    #allowed_to_eat = fields.Boolean(string='Puede comer', default=True)

    @api.onchange("cedula")
    def _compute_lunch_parameters(self):

        for rec in self:
            employee_obj = self.env['hr.employee'].search([('identification_id', '=', rec.cedula)], limit=1)
            contact_obj = self.env['res.partner'].search([('vat', '=', rec.cedula)], limit=1)

            #employee_id_format = #TODO: FORMAT CEDULA
            if employee_obj and rec.cedula:
                rec.first_name = employee_obj.name
                rec.last_name = employee_obj.last_name
                rec.unit = employee_obj.department_id.name

            elif contact_obj and rec.cedula:    
                rec.first_name = contact_obj.firstname
                rec.last_name = contact_obj.lastname
                rec.contact_object = contact_obj.id
                rec.unit = "VICEMINISTERIO ADMINISTRATIVO"

    #Working on this
    # def is_allowed_to_eat(self):
    #     """Grant access to the collaborator to be able to eat"""
    #     if self.allowed_to_eat:
    #         if self.employee_object:
    #             return self.employee_object.active and (datetime.today() >= self.employee_object.enter_date and datetime.today() <= self.employee_object.end_date)
    #         else:
    #             return self.from_date <= datetime.today() <= self.date_to
    #     else:
    #         return False

    @api.depends('first_name', 'last_name')
    def _compute_rec_name(self):
        """Set rec_name as a full name throughout the name field"""
        for rec in self:
            rec.name = f"{self.first_name} {self.last_name}"
            return rec.name
