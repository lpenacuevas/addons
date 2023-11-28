# -*- coding: utf-8 -*-
from odoo import models, fields, api


class staff_actions(models.Model):
    _name = 'staff.action'
    _description = 'accion de personal'

    # _inherits = {"res.partner": "partner_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]

    date_staff = fields.Date('Fecha accion', required=True)
    effective_date = fields.Date('Fecha efectividad', required=True)
    action_motivation = fields.Text('Motivo de accion', required=True)

    action_type_id = fields.Many2one(
        "action.type",
        string='Tipo accion',
        required=True
    )

    name = fields.Many2one(
        'action.detail',
        string='Detalle accion',
        domain="[('action_type_id', '=', action_type_id)]",
        required=True
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado',
        required=True
    )

    jobs_id = fields.Many2one(
        'hr.job',
        string="Cargo",
        compute="_job_field"
    )

    departaments_id = fields.Many2one(
        'hr.department',
        string="Departamento",
        compute="_department_field"
    )
    id_mrh = fields.Integer()

    @api.depends('employee_id.job_id')
    def _job_field(self):
        for record in self:
            record.jobs_id = record.employee_id.job_id

    @api.depends('employee_id.department_id')
    def _department_field(self):
        for record in self:
            record.departments_id = record.employee_id.department_id

    @api.model
    def _default_stage_id(self):
        Stage = self.env["staff.action.stage"]
        return Stage.search([("state", "=", "new")],
                            limit=1)

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)

    stage_id = fields.Many2one(
        "staff.action.stage",
        default=_default_stage_id,
        group_expand="_group_expand_stage_id")

    state = fields.Selection(related="stage_id.state")

    def button_done(self):
        Stage = self.env["staff.action.stage"]
        done_stage = Stage.search([("state", "=", "done")],
                                  limit=1)
        for checkout in self:
            checkout.stage_id = done_stage
        return True
