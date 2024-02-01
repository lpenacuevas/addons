from odoo import models, fields, api


class hr_job(models.Model):
    _inherit = "hr.job"

    grupo_ocupacional = fields.Many2one(
        "occupational.group", string="Grupo ocupacional", required=True)
    group_viatico = fields.Many2one(
        "cargo.viatico", string="Grupo viatico", required=True)
    id_mrh = fields.Integer()

    request_list_details_ids = fields.One2many('request.list.details', 'job_id', string="Lista de solicitudes")
