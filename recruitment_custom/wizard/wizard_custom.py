from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class WizardCustom(models.TransientModel):
    _name = 'wizard.custom'

    # _inherits = {"res.partner": "partner_id"}
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
        # domain="[('action_type_id', '=', action_type_id)]",
        required=True
    )

    name = fields.Char('Nombres', required=True)
    lastname = fields.Char('Apellidos', required=True)

    # applicant_id = fields.Many2one('partner.applicant', string='Nombre del Candidato', required=True)

    departments_id = fields.Many2one(
        'hr.department',
        string="Departamento",
    )

    position_id = fields.Many2one(
        'hr.job',
        string="Cargo",
    )
    is_created = fields.Boolean(
        string='Novedad creada', copy=False, default=False)

    salary = fields.Float('Sueldo')

    condition_type_id = fields.Many2one(
        "condition.types",
        string='Tipo de condicion'
    )
    employee_type_id = fields.Many2one(
        "employee.types",
        string="Tipo de empleado"
    )

    identification = fields.Char(string='Nº identificación')
    passport = fields.Char(string='Nº Pasaporte')
    country_id = fields.Many2one('res.country', string='País de nacimiento')
    gender = fields.Selection(
        string='Género',
        selection=[('male', 'Masculino'),
                   ('female', 'Femenino'), ('other', 'Otro')])

    sequence = fields.Char(string='No. de accion ', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: self.env['ir.sequence'].next_by_code('staff.action') or _('New'))

    def save_staff_action(self):
        self.is_created = True
        record = self.env['hr.applicant'].browse(
            self._context.get('active_id'))
        record.write({'is_created': self.is_created})
        self.env['applicant.action'].create({
            'date_staff': self.date_staff,
            'effective_date': self.effective_date,
            'action_motivation': self.action_motivation,
            'action_type_id': self.action_type_id.id,
            'action_detail': self.action_detail_id.id,
            # 'applicant_name_id': self.applicant_id.name,
            'departments_id': self.departments_id.id,
            'jobs_id': self.position_id.id,
            'salary': self.salary,
            'sequence': self.sequence,
            'name': self.name,
            'lastname': self.lastname,
            'condition_type_id': self.condition_type_id.id,
            'employee_type_id': self.employee_type_id.id
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
            'report_name': 'recruitment_custom.staff_action_report_minister',
            'report_type': 'qweb-pdf',
        }

    def print_action_rh(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'recruitment_custom.staff_action_report_rh',
            'report_type': 'qweb-pdf',
        }
