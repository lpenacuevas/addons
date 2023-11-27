from odoo import models, fields, api


class action_type(models.Model):
    _name = 'action.type'
    _description = 'Tipos de acciones de personal'

    name = fields.Char("Tipo de action", required=True)
    
    id_mrh = fields.Integer()