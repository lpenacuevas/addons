from odoo import api, exceptions, fields, models

class Visitante_Line(models.Model):
    _name = "visitante.line"
    _description = "Visitantes Line"

    visitante_id = fields.Many2one(
        "visitante",
        required=True,
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado'
        )

    departments_name = fields.Char(        
        string="Departamento",
        readonly=True
    )

    piso_no = fields.Char(
    string="Piso",
    readonly=True)


    @api.onchange('employee_id')
    def _change_field(self):
        for record in self:
            if record.employee_id:
                dp = self.env['hr.department'].search([('id', '=', record.employee_id.department_id.id)], limit=1)
                record.piso_no = dp[0].piso_id.name
                record.departments_name = dp[0].name
