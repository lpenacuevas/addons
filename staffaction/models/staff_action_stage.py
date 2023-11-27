from odoo import fields, models


class staff_action_stage(models.Model):
    _name = "staff.action.stage"
    _description = "StaffAction Stage"
    _order = "sequence"

    name = fields.Char('Estados')
    sequence = fields.Integer('Secuencia',default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [("open", "En Proceso"),
         ("done", "Completada"),
         ("cancel", "Cancelada")],
        default="new",
    )



