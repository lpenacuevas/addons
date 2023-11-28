from odoo import api, fields, models


class PartnerFamily(models.Model):
    _name = 'partner.family'

    name = fields.Char('Nombre Completo')
    relationship = fields.Char('Parentesco')
    gender = fields.Selection([
        ('male', 'Masculino'),
        ('female', 'Femenino'),
        ('other', 'Otro')
    ], tracking=True, string='Género')
    age = fields.Integer(
        string='Edad')
    partner_id = fields.Many2one('partner.applicant', ondelete='cascade', string='Candidatos')
    color = fields.Integer(string='Color Index', default=0)


class PartnerReferences(models.Model):
    _name = 'partner.references'

    name = fields.Char('Nombre Completo')
    phone_number = fields.Char('Telefonos')
    partner_references_id = fields.Many2one('partner.applicant', ondelete='cascade', string='Candidatos')
