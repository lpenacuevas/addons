from odoo import api, fields, models


class HrLeave(models.Model):
    _inherit = 'hr.leave.type'

    type_vacation = fields.Selection([('leave', 'Permiso'), ('license', 'Licencias'), ('vacation', 'Vacaciones')],
                                     default='leave',
                                     string="Tipo de permiso",
                                     help="Whether this should be computed as a holiday or as work time (eg: formation)")

    @api.onchange('type_vacation')
    def _compute_time_type(self):
        for rec in self:
            if rec.type_vacation == 'vacation' or rec.type_vacation == 'license':
                rec.time_type = 'other'
            else:
                rec.time_type = 'leave'
