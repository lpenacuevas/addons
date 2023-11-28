# -*- coding: utf-8 -*-
from odoo import models, fields, api


class localidades(models.Model):
    _name = 'localidades.localidades'
    _description = 'mantenimiento de localidades'

    # _inherits = {"res.partner": "partner_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    name = fields.Char()
    direccion = fields.Text()
    telefono = fields.Char()
    num_localidades = fields.Integer(compute = "_compute_num_localidad")

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
    #@api.depends('line_ids')
    def _compute_num_localidad(self):
     for record in self:
        record.num_localidades = record.num_localidades + 1

    
        