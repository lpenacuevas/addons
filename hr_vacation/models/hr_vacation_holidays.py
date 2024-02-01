from odoo import api, fields, models

class HrVacationHoliday(models.Model):
    _name = 'hr.vacation.holiday'
    _description = 'This module is to manage all yearly holidays from a country'

    name = fields.Char('Festividad')
    date = fields.Date('Fecha')

