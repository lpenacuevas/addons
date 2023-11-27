from odoo import models, fields, api

class occupational(models.Model):
    _name = 'occupational.group'
    _description = 'Grupo Ocupacional'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    name = fields.Char("Grupo ocupacional", required=True)
    nivel = fields.Char("Nivel", required=True)
    ponderacion = fields.Integer()
    id_mrh = fields.Integer()
    
    
    
    
    
    