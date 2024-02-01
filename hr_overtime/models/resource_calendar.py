from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    time_per_week = fields.Float('Promedio de horas semanales', readonly=True)

    @api.onchange('labor_ids')
    def _get_time_per_week(self):
        for rec in self:
            if rec.labor_ids:
                total_hours = 0.0
                for line in rec.labor_ids:
                    if line.hour_to and line.hour_from:
                        total_hours += line.hour_to - line.hour_from
                rec.time_per_week = total_hours
                logging.info(rec.time_per_week)

