from odoo import models, fields, api


class condition_type(models.Model):
    _name = 'condition.types'
    _description = 'Tipo de condicion del empleado'

    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Tipo condicion")
    id_mrh = fields.Integer()
