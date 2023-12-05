from odoo import api, fields, models
from odoo.exceptions import UserError


class WizardCustom(models.TransientModel):
    _name = 'wizard.custom'

    # _inherits = {"res.partner": "partner_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]

    date_staff = fields.Date('Fecha de accion', required=True)
    effective_date = fields.Date('Fecha efectividad', required=True)
    action_motivation = fields.Text('Motivo de accion', required=True)
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

    applicant_id = fields.Many2one(
        'partner.applicant', string='Nombre del Candidato', required=True)

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

    # def print_staff_action(self):
    #     """This return the action of the report for any staff action"""
    #     return self.env.ref('staff_action_report').report_action(self)

    # @api.onchange('effective_date')
    # def validation_date(self):
    # """This show the user they need to use an effective date greater than the date of the action"""
    # for rec in self:
    #     if rec.effective_date > rec.date_staff:
    #       raise UserError("La fecha efectiva necesita ser mayor a la fecha de creación de la novedad")

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
            'name': self.action_detail_id.id,
            'applicant_id': self.applicant_id.id,
            'departments_id': self.departments_id.id,
            'jobs_id': self.position_id.id,
            'salary': self.salary
        })
        return

    @api.constrains('date_staff', 'effective_date')
    def _check_staff_dates(self):
        for rec in self:
            if rec.date_staff > rec.effective_date:
                raise UserError('La fecha efectiva debe ser mayor o igual a la fecha de la accion')
