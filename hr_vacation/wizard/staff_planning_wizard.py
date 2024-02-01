from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class StaffActionPlanningWizard(models.TransientModel):
    _name = 'staff.planning.wizard'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    date_staff = fields.Date('Fecha de accion', required=True)
    effective_date = fields.Date('Fecha efectividad', required=True)
    action_motivation = fields.Text('Motivo de accion')
    action_type_id = fields.Many2one(
        "action.type",
        string='Tipo de accion',
        required=True
    )

    action_detail_id = fields.Many2one(
        'action.detail',
        string='Detalle',
        required=True,
        domain="[('action_type_id', '=', action_type_id)]"
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado',
        required=True
    )

    departments_id = fields.Many2one(
        'hr.department',
        string="Departamento",
    )

    position_id = fields.Many2one(
        'hr.job',
        string="Cargo",
    )
    is_created = fields.Boolean(
        string='Novedad creada')

    salary = fields.Float('Sueldo')

    sequence = fields.Char(string='No. de accion ', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: self.env['ir.sequence'].next_by_code('staff.action') or _('New'))

    def save_staff_action(self):
        self.is_created = True
        self.env['hr.vacation.planning'].browse(
            self._context.get('active_id')).write({'is_created': self.is_created})
        self.env['staff.action'].create({
            'date_staff': self.date_staff,
            'effective_date': self.effective_date,
            'action_motivation': self.action_motivation,
            'action_type_id': self.action_type_id.id,
            'name': self.action_detail_id.id,
            'employee_id': self.employee_id.id,
            'departments_id': self.departments_id.id,
            'jobs_id': self.position_id.id,
            'salary': self.salary,
            'sequence': self.sequence
        })
        return

    @api.constrains('date_staff', 'effective_date')
    def _check_staff_dates(self):
        for rec in self:
            if rec.date_staff > rec.effective_date:
                raise UserError('La fecha efectiva debe ser mayor o igual a la fecha de la accion')

    def print_action_minister(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'staffaction.staff_action_report_latest',
            'report_type': 'qweb-pdf',
        }

    def print_action_rh(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'staffaction.staff_action_report',
            'report_type': 'qweb-pdf',
        }
