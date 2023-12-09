import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class almuerzo(models.Model):
    _name = 'almuerzo.almuerzo'
    _description = 'Modelo de almuerzo'
    
    cedula = fields.Char("Cedula")
    first_name = fields.Char("Nombre")
    last_name = fields.Char("Apellidos")
    name = fields.Char("Nombre completo", store=True, compute="_compute_rec_name")
    quantity = fields.Integer("Cantidad", default="1")
    from_date = fields.Date("Fecha desde")
    date_to = fields.Date("Fecha hasta")
    employee_object = fields.Many2one("hr.employee")
    contact_object = fields.Many2one("res.partner")
    person_type_id = fields.Many2one("almuerzo.tipo.persona", string="Tipo de persona")
    unit = fields.Char("Unidad")



    @api.onchange("cedula")
    def _compute_lunch_parameters(self):

        for rec in self:
            employee_obj = self.env['hr.employee'].search([('identification_id', '=', rec.cedula)], limit=1)
            contact_obj = self.env['res.partner'].search([('vat', '=', rec.cedula)], limit=1)
            

            #employee_id_format = #TODO: FORMAT CEDULA
            if employee_obj and rec.cedula:
                rec.first_name = employee_obj.name
                rec.last_name = employee_obj.last_name
                rec.contact_object = False
                rec.unit = employee_obj.department_id.name

            
            elif contact_obj and rec.cedula:    
                rec.first_name = contact_obj.firstname
                rec.last_name = contact_obj.lastname
                rec.contact_object = contact_obj.id


    @api.depends('first_name', 'last_name')
    def _compute_rec_name(self):
        """Set rec_name as a full name throughout the name field"""
        for rec in self:
            rec.name = f"{self.first_name} {self.last_name}"
            return rec.name


#TODO: Crear logica para permitir el almuerzo tomando como parámetros las fechas
#TODO: Crear alerta de acceso permitido (Verde) o denegado (Roja). Si es denegado debe de lanzar una excepcion.
#TODO: Pantalla principal --> Nombre,apellido 
#TODO: Crear la vista de lista para el registro de cada persona (Nombre, apellido, departamento, tipo de persona). Nota: Si es personal externo el departamento es el dept administrativo


    # THIS Works
    # @api.onchange("cedula")
    # def _change_fields(self):
    #     for rec in self:
    #         # Getting contact object list by cedula
    #         contact_obj = self.env['res.partner'].search([('vat', '=', rec.cedula)], limit=1)
    #         _logger.info(f"--------------ENTRO------------------")
    #         _logger.info(f"-------------{rec}------------------")
    #         _logger.info(f"-------------{rec.cedula}------------------")
    #         _logger.info(f"-------------{rec.name}------------------")

    #         if contact_obj and rec.cedula:
    #             rec.name = contact_obj.firstname
    #             rec.last_name = contact_obj.lastname
                # raise UserError("User Error")