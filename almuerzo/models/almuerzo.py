import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class almuerzo(models.Model):
    _name = 'almuerzo.almuerzo'
    _description = 'Modelo de almuerzo'
    
    cedula = fields.Char("Cédula")
    first_name = fields.Char("Nombre")
    last_name = fields.Char("Apellidos")
    name = fields.Char("Nombre completo", store=True, compute="_compute_rec_name")
    quantity = fields.Integer("Cantidad", default="1")
    from_date = fields.Date("Fecha desde")
    date_to = fields.Date("Fecha hasta")
    person_type_id = fields.Many2one("almuerzo.tipo.persona", string="Tipo de persona")
    contact_object = fields.Many2one("res.partner")
    unit = fields.Char("Unidad", default= lambda self: self.env['hr.department'].search([('id_mrh', '=', '37')]).name)
    comment = fields.Char("Comentario")



    @api.onchange("cedula")
    def _compute_lunch_parameters(self):

        for rec in self:
            if not rec.cedula:
                return
            
            formatted_cedula = rec.cedula.replace('-', '')
            rec.cedula = formatted_cedula

            contact_obj = self.env['res.partner'].search([('vat', '=', formatted_cedula), ('vat', '!=', '')], limit=1)
            
            if contact_obj.name:
                rec.first_name = contact_obj.firstname
                rec.last_name = contact_obj.lastname
                rec.contact_object = contact_obj.id
                rec.unit = self.env['hr.department'].search([('id_mrh', '=', '37')]).name


    @api.depends('first_name', 'last_name')
    def _compute_rec_name(self):
        """Set rec_name as a full name throughout the name field"""
        for rec in self:
            rec.name = f"{self.first_name} {self.last_name}"
            return rec.name


#TODO: Modificar nombre del modelo a almuerzo.administracion y la descripción a Administración de almuerzo
#TODO: Establecer los campos requeridos