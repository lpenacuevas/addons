from odoo import models, fields

class tipo_persona(models.Model):
    _name = "almuerzo.tipo.persona"
    _description = "Mantenimiento para capturar los tipos de persona del modulo de control de almuerzo"

    name = fields.Char("Tipo de persona")