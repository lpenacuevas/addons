from odoo import models, fields, api


class ApplicantAction(models.Model):
    _name = 'applicant.action'
    _description = 'gestion de accion de personal para candidatos'

    # _inherits = {"res.partner": "partner_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]

    date_staff = fields.Date('Date Action', required=True)
    effective_date = fields.Date('Fecha efectividad', required=True)
    action_motivation = fields.Text('Motivo de accion', required=True)
    action_type_id = fields.Many2one(
        "action.type",
        string='Tipo de accion',
        required=True
    )

    name = fields.Many2one(
        'action.detail',
        string='Detalle',
        domain="[('action_type_id', '=', action_type_id)]",
        required=True
    )


    jobs_id = fields.Many2one(
        'hr.job',
        string="Cargo",
    )

    applicant_id = fields.Many2one(
        'res.partner',
        string='Candidato'
    )

    departments_id = fields.Many2one(
        'hr.department',
        "Departamento",
    )

    state = fields.Selection(related="stage_id.state")
    id_mrh = fields.Integer()

    @api.model
    def _default_stage_id(self):
        Stage = self.env["staff.action.stage"]
        return Stage.search([("state", "=", "new")],
                            limit=1)

    stage_id = fields.Many2one(
        "staff.action.stage",
        default=_default_stage_id,
        group_expand="_group_expand_stage_id")

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)

    def button_done(self):
        Stage = self.env["staff.action.stage"]
        done_stage = Stage.search([("state", "=", "done")],
                                  limit=1)
        for checkout in self:
            checkout.stage_id = done_stage
        return True




