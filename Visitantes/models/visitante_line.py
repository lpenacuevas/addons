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
        string="Departamento", store=True)

    piso_no = fields.Char(
    string="Piso", store=True)

    @api.onchange('employee_id')
    def _change_field(self):
        for record in self:
            if record.employee_id:
                record.piso_no = record.employee_id.department_id.piso_id.id
                record.departments_name = record.employee_id.department_id.name