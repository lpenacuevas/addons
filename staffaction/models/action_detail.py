# import json
import logging
# import requests

from odoo import models, fields, api
# from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class action_detail(models.Model):
    _name = 'action.detail'
    _description = 'Detalles de los tipos de accion'

    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Detalles de acciones", required=True)

    action_type_id = fields.Many2one(
        "action.type",
        string='Tipo accion',
        required=True
    )
    id_mrh = fields.Integer()

    @api.onchange('name')
    def _type_action_hidden(self):
        _logger.info("Cumplio")
        for data in self:
            if data.name:
                _logger.info("Cumplio")
            else:
                _logger.info("No Cumplio")
