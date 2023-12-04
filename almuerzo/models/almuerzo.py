from odoo import models, fields, api


class almuerzo(models.Model):
    _name = 'almuerzo'
    _description = 'Modelo de almuerzo'

    name = fields.Char("Test")
