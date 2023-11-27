import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Department(models.Model):
    _inherit = 'hr.department'

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for department in self:
            department.complete_name = department.name
