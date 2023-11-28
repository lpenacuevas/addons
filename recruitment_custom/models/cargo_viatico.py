from odoo import models, fields, api

class cargo_viatico(models.Model):
    _name = 'cargo.viatico'
    _description = ''
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Grupos")
    desayuno = fields.Float("Desayuno", digits=(12,2))
    almuerzo = fields.Float("Almuerzo", digits=(12,2))
    cena = fields.Float("Cena", digits=(12,2))
    alojamiento = fields.Float("Alojamiento", digits=(12,2))
    id_mrh = fields.Integer()
