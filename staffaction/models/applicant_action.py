from odoo import models, fields, api
import logging

logger = logging.getLogger(__name__)


class ApplicantAction(models.Model):
    _name = 'applicant.action'
    _description = 'gestion de accion de personal para candidatos'

    # _inherits = {"res.partner": "partner_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]

    date_staff = fields.Date('Date Action', required=True)
    effective_date = fields.Date('Fecha efectividad', required=True)
    action_motivation = fields.Text('Motivo de accion')
    action_type_id = fields.Many2one(
        "action.type",
        string='Tipo de accion',
        required=True
    )

    action_detail = fields.Many2one(
        'action.detail',
        string='Detalle',
        domain="[('action_type_id', '=', action_type_id)]",
        required=True
    )

    jobs_id = fields.Many2one(
        'hr.job',
        string="Cargo",
    )

    # applicant_id = fields.Many2one(
    #     'partner.applicant',
    #     string='Candidato'
    # )

    name = fields.Char(string='Nombres')
    lastname = fields.Char(string='Apellidos')

    departments_id = fields.Many2one(
        'hr.department',
        "Departamento",
    )

    state = fields.Selection(related="stage_id.state")
    id_mrh = fields.Integer()

    salary = fields.Float('Sueldo')

    condition_type_id = fields.Many2one(
        "condition.types",
        string='Tipo de condicion'
    )
    employee_type_id = fields.Many2one(
        "employee.types",
        string="Tipo de empleado"
    )

    @api.model
    def _default_stage_id(self):
        Stage = self.env["staff.action.stage"]
        return Stage.search([("state", "=", "open")],
                            limit=1)

    stage_id = fields.Many2one(
        "staff.action.stage",
        default=_default_stage_id,
        group_expand="_group_expand_stage_id")

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)

    sequence = fields.Char(string='No. de accion ', required=True, copy=False, readonly=True, index=True)

    def staff_action_done(self):
        for rec in self:
            if rec.state == "open":
                rec.write({'stage_id': rec.env["staff.action.stage"].search([("state", "=", "done")])})
                rec.env['hr.employee'].create({
                    'name': rec.name,
                    'last_name': rec.lastname,
                    'job_id': rec.jobs_id.id,
                    'department_id': rec.departments_id.id,
                    'salary': rec.salary,
                    'tipo_condicion': rec.condition_type_id.id,
                    'tipo_empleado': rec.employee_type_id.id,
                    'enter_date': rec.effective_date
                })

                rec.env['res.partner'].create({
                    'company_type': 'person',
                    'firstname': rec.name,
                    'lastname': rec.lastname,
                })
                message_body = (f"Empleado creado: {rec.name} {rec.lastname}<br/>"
                                f"<li><i::marker/>Departamento: {rec.departments_id.name}<br/>"
                                f"<li><i::marker/>Cargo:\n{rec.jobs_id.name}<br/>"
                                f"<li><i::marker/>Salario:\n{rec.salary}<br/>"
                                f"<li><i::marker/>Tipo de condición:\n{rec.condition_type_id.name}<br/>"
                                f"<li><i::marker/>Tipo de empleado:\n{rec.employee_type_id.name}<br/>")
                rec.message_post(body=message_body)

    def staff_action_cancel(self):
        for rec in self:
            if rec.state == "open":
                rec.write({'stage_id': rec.env["staff.action.stage"].search([("state", "=", "cancel")])})
                message_body = f"La acción de personal para {rec.name} {rec.lastname} ha sido cancelada.<br/>"
                rec.message_post(body=message_body)
