from odoo import api, fields, models


class PartnerAcademyRecord(models.Model):
    _name = 'partner.academy.record'
    _description = 'PartnerAcademyRecord'

    level = fields.Selection(
        string='Nivel',
        selection=[('literate', 'Alfabetizado'),
                   ('basic', 'Nivel Basico'), ('medium', 'Nivel Medio'), ('university', 'Grado Universitario'),
                   ('post-grade', 'Postgrado'), ('master', 'Maestria'), ('doctorate', 'Doctorado')])

    major = fields.Char('Carrera')
    master = fields.Char('Maestria')
    post_grade = fields.Char('Titulo Obtenido')
    doctorate = fields.Char('Doctorado')

    status = fields.Selection(
        string='Estado',
        selection=[('process', 'En Proceso'),
                   ('done', 'Concluido'), ],
        required=False, )

    partner_academy_id = fields.Many2one('partner.applicant', ondelete='cascade', string='Candidatos')
