from odoo import models, fields, api

class horaslabor(models.Model):
    _name = 'horas.labor'
    _description = ''

    _inherit = 'resource.calendar.attendance'

    
    name = fields.Char("detalle")
    calendar_id = fields.Many2one(
        "resource.calendar",
        required=True,
    )