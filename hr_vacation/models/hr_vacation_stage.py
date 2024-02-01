from odoo import fields, models


class HrVacationStage(models.Model):
    _name = "hr.vacation.stage"
    _order = "sequence"

    name = fields.Char('Etapas')
    sequence = fields.Integer('Secuencia', default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [("to approved", "Por Aprobar"),
         ("approved", "Aprobadas"),
         ("cancel", "Canceladas")],
        default="to approved",
    )
