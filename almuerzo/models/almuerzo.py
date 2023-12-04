from odoo import models, fields, api


class almuerzo(models.Model):
    _name = 'almuerzo'
    _description = 'Modelo de almuerzo'

    # name = fields.Char("test")
    
    cedula = fields.Char("Cedula")
    name = fields.Char("Nombre")
    last_name = fields.Char("Apellidos")
    quantity = fields.Integer("Cantidad")
    from_date = fields.Date("Fecha desde")
    date_to = fields.Date("Fecha hasta")
