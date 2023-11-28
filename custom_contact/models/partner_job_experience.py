from odoo import api, fields, models


class PartnerJobExperience(models.Model):
    _name = 'partner.job.experience'

    name = fields.Char('Empresa u Organizacion:')
    job_position = fields.Char('Cargo Desempeñado:')
    enter_date = fields.Date('Desde:')
    end_date = fields.Date('Hasta:')
    salary = fields.Integer('Salario Devengado')

    partner_relate_id = fields.Many2one('partner.applicant', ondelete='cascade', string='Candidatos')


class PartnerComplementaryExperience(models.Model):
    _name = 'partner.complementary.experience'

    name = fields.Char('Curso Realizado')
    school = fields.Char('Entidad Educativa')

    partner_complementary_id = fields.Many2one('partner.applicant', ondelete='cascade', string='Candidatos')
