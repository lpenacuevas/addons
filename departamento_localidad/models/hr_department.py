from odoo import models, fields, api


class hr_department(models.Model):
    _inherit = "hr.department"
#     _description = 'departamento_localidad.departamento_localidad'    
    localidad_id = fields.Many2one(
        "localidades.localidades",
        "Localidades",
        required=True,
        )
    piso_id = fields.Many2one(
        "localidad.piso",
        "Piso",
        required=True,
        )
    abreviatura = fields.Char(required = True)

    id_mrh = fields.Integer()   

