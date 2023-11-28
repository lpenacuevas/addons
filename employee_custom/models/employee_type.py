from odoo import models, fields, api


class employee_type(models.Model):
    _name = "employee.types"
    _description = 'Tipo de empleado'

    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Tipo empleado")
    id_mrh = fields.Integer()