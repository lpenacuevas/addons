from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"
    #     _description = 'departamento_localidad.departamento_localidad'

    custom_contact_type_selection = fields.Selection(
        [('CIVIL', 'CIVIL'), ('CARRERA', 'CARRERA'), ('MILITAR', 'MILITAR')], "Condicion")

    reference_spot = fields.Char('Punto de Referencia')

    def compute_applicant_from_partner(self):
        excluded_fields = [
            '__last_update', 'create_date', 'write_date', 'id', 'display_name',
            'message_last_post', 'message_follower_ids'
        ]
        context = {}
        applicant_fields = self.env['partner.applicant']._fields.keys()
        for field_name, field_value in self._fields.items():
            if field_name not in excluded_fields:
                if field_name in applicant_fields:
                    context['default_applicant_id'] = self.id
                    if isinstance(field_value, fields.Many2one):
                        related_object = getattr(self, field_name)
                        context[f'default_{field_name}'] = related_object.id if related_object else False
                    elif isinstance(field_value, (fields.One2many, fields.Many2many)):
                        related_objects = getattr(self, field_name)
                        context[f'default_{field_name}'] = [(6, 0, related_objects.ids)]
                    else:
                        context[f'default_{field_name}'] = getattr(self, field_name)
        return {
            'name': 'Crear Aplicante',
            'type': 'ir.actions.act_window',
            'res_model': 'partner.applicant',
            'view_mode': 'form',
            'target': 'new',
            'context': context,
        }
