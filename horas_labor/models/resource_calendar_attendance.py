from odoo import models, fields, api


class resource_calendar_attendance(models.Model):
    _inherit = "resource.calendar"
#     _description = 'departamento_localidad.departamento_localidad'    
   
    labor_ids = fields.One2many('horas.labor', 'calendar_id', string="horas de labor")