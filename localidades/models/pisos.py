from odoo import models, fields

class piso(models.Model):
    _name = 'localidad.piso'
    _description = 'Piso en donde se encuentra una unidad que tiene una localidad'

    # _inherits = {"res.partner": "partner_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Piso')
    numero = fields.Char('Numero de piso')

