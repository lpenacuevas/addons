# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import datetime
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class staff_action(models.Model):
    _name = 'staff.action'
    _description = 'Accion de personal'
    _rec_name = 'employee_id'

    # _inherits = {"res.partner": "partner_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]

    date_staff = fields.Date('Fecha Accion', required=True)
    effective_date = fields.Date('Fecha efectividad', required=True)
    action_motivation = fields.Text('Motivo de accion')
    action_type_id = fields.Many2one(
        "action.type",
        'Tipo de Accion',
        required=True,
    )

    action_detail = fields.Many2one(
        'action.detail',
        string='Detalle',
        required=True,
        domain="[('action_type_id', '=', action_type_id)]"
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado')

    jobs_id = fields.Many2one(
        'hr.job',
        string="Cargo",
        readonly=False
    )

    applicant_id = fields.Many2one(
        comodel_name='res.partner',
        string='Empleado'
    )

    departments_id = fields.Many2one(
        'hr.department',
        string="Department",
        readonly=False
    )

    salary = fields.Float('Sueldo')

    @api.onchange('employee_id')
    def _job_field(self):
        for record in self:
            if record.employee_id:
                id_job = record.employee_id.job_id.id
                record.jobs_id = id_job
                id_department = record.employee_id.department_id.id
                record.departments_id = id_department
                record.salary = record.employee_id.salary

    state = fields.Selection(related="stage_id.state", string='Estado')

    @api.model
    def _default_stage_id(self):
        Stage = self.env["staff.action.stage"]
        return Stage.search([("state", "=", "open")],
                            limit=1)

    stage_id = fields.Many2one(
        "staff.action.stage",
        default=_default_stage_id,
        group_expand="_group_expand_stage_id",
    )

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)

    def staff_action_done(self):
        for rec in self:
            if rec.state == "open":
                rec.write({'stage_id': rec.env["staff.action.stage"].search([("state", "=", "done")])})
                updated_employee = rec.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
                updated_employee.write({
                    'job_id': rec.jobs_id.id,
                    'department_id': rec.departments_id.id,
                    'salary': rec.salary
                })
                message_body = (f"<li><i::marker/>Tipo de acción: {rec.action_type_id.name}<br/>"
                                f"<li><i::marker/>Detalle de acción: {rec.action_detail.name}<br/>"
                                f"<li><i::marker/>Etapa:\n{rec.stage_id.name}<br/>"
                                f"<li><i::marker/>Departamento: {rec.departments_id.name}<br/>"
                                f"<li><i::marker/>Cargo:\n{rec.jobs_id.name}<br/>"
                                )
                rec.message_post(body=message_body)

    sequence = fields.Char(string='No. de accion ', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('staff.action') or 'New'
        res = super(staff_action, self).create(vals)
        for rec in res:
            if rec.departments_id.id == rec.employee_id.department_id.id:
                message_body = (f"<li><i::marker/>Tipo de acción: {rec.action_type_id.name}<br/>"
                                f"<li><i::marker/>Detalle de acción: {rec.action_detail.name}<br/>"
                                f"<li><i::marker/>Etapa:\n{rec.stage_id.name}<br/>")
                rec.message_post(body=message_body)
        return res

    def staff_action_cancel(self):
        for rec in self:
            if rec.state == "open":
                rec.write({'stage_id': rec.env["staff.action.stage"].search([("state", "=", "cancel")])})

    @api.constrains('date_staff', 'effective_date')
    def _check_staff_dates(self):
        for rec in self:
            if rec.date_staff > rec.effective_date:
                raise UserError('La fecha efectiva debe ser mayor o igual a la fecha de la accion')
