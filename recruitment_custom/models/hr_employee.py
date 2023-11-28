from odoo import models, fields, api


class custom_hr_employee(models.Model):
    _inherit = "hr.employee"
#     _description = 'departamento_localidad.departamento_localidad'    
   
    custom_employee_type_selection = fields.Selection([('FIJO', 'FIJO'), ('CONTRATADO','CONTRATADO')], "Type")