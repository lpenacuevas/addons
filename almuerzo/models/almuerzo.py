import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class almuerzo(models.Model):
    _name = 'almuerzo.almuerzo'
    _description = 'Modelo de almuerzo'
    _rec_name = 'cedula'

    # name = fields.Char("test")
    
    cedula = fields.Char("Cedula")
    name = fields.Char("Nombre")
    last_name = fields.Char("Apellidos")
    quantity = fields.Integer("Cantidad", default="1")
    from_date = fields.Date("Fecha desde")
    date_to = fields.Date("Fecha hasta")
    employee_object = fields.Many2one("hr.employee")
    contact_object = fields.Many2one("res.partner")


    @api.onchange("cedula")
    def _compute_lunch_parameters(self):

        for rec in self:
            employee_obj = self.env['hr.employee'].search([('identification_id', '=', rec.cedula)], limit=1)
            contact_obj = self.env['res.partner'].search([('vat', '=', rec.cedula)], limit=1)
            

            #employee_id_format = #TODO: FORMAT CEDULA
            if employee_obj and rec.cedula:
                rec.name = employee_obj.name
                rec.last_name = employee_obj.last_name
                rec.contact_object = False
                
            
            elif contact_obj and rec.cedula:    
                rec.name = contact_obj.firstname
                rec.last_name = contact_obj.lastname
                rec.contact_object = contact_obj.id
                _logger.info(f"-------------{rec.contact_object.id}------------------")

    

#TODO: Cambiar rec_name, comcapt name,last_name
#TODO: Crear logica para permitir el almuerzo tomando como parámetros las fechas
#TODO: Crear alerta de acceso permitido (Verde) o denegado (Roja). Si es denegado debe de lanzar una excepcion.
#TODO: Pantalla principal --> Nombre,apellido 
#TODO: Cuando es empleado debe de traer el departamento
#TODO: Crear campo tipo de persona Many2one relacionado con el mantenimiento de tipo de persona
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