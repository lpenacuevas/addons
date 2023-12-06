from odoo import models, fields, api


class almuerzo(models.Model):
    _name = 'almuerzo.almuerzo'
    _description = 'Modelo de almuerzo'
    _rec_name = 'cedula'

    # name = fields.Char("test")
    
    cedula = fields.Char("Cedula", store=True, compute='_change_fields')
    name = fields.Char("Nombre")
    last_name = fields.Char("Apellidos")
    quantity = fields.Integer("Cantidad")
    from_date = fields.Date("Fecha desde")
    date_to = fields.Date("Fecha hasta")


#TODO: Validar cedula con maestro de contactos
#TODO: Validar cedula con maestro de empleados
#TODO: Mantenimiento tipo de empleado


# WORKIN ON THIS
# @api.onchange("cedula")
# def _change_fields(self):
#     # Getting contact object list by cedula
#     contact_obj = self.env['res.partner'].search([('vat', '=', self.cedula)], limit=1)

#     # Itering on records in the contact object
#     for rec in contact_obj:
#         if rec:
#             self.name = rec.first_name
#             self.last_name = rec.last_name
#             # rec.write({"cedula": self.cedula})



# def change_visitor_status(self):
#     for rec in self:
#         record = rec.env['visitante'].browse(rec._context.get('active_id'))
#         status_tag = rec.env['tags.visitantes'].search([('name', '=', 'Salida')], limit=1)
#     if record and status_tag:
#         record.write({'state': [(6, 0, [status_tag.id])]})