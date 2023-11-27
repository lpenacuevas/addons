from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Skill(models.Model):
    _name = 'res.skill'
    _description = "Skill"

    name = fields.Char(required=True, string='Habilidad')
    skill_type_id = fields.Many2one('res.skill.type', ondelete='cascade', string='Tipo de Habilidad')


class PartnerSkill(models.Model):
    _name = 'res.partner.skill'
    _description = "Skill level for an employee"
    _rec_name = 'skill_id'
    _order = "skill_level_id"

    partner_id = fields.Many2one('partner.applicant', required=True, ondelete='cascade')
    skill_id = fields.Many2one('res.skill', required=True, string='Habilidad')
    skill_level_id = fields.Many2one('res.skill.level', required=True, string='Nivel de Habilidad')
    skill_type_id = fields.Many2one('res.skill.type', required=True, string='Tipo de Habilidad')
    level_progress = fields.Integer(related='skill_level_id.level_progress', string='Progreso')

    _sql_constraints = [
        ('_unique_skill', 'unique (employee_id, skill_id)', "Two levels for the same skill is not allowed"),
    ]

    @api.constrains('skill_id', 'skill_type_id')
    def _check_skill_type(self):
        for record in self:
            if record.skill_id not in record.skill_type_id.skill_ids:
                raise ValidationError(
                    _("The skill %(name)s and skill type %(type)s doesn't match", name=record.skill_id.name,
                      type=record.skill_type_id.name))

    @api.constrains('skill_type_id', 'skill_level_id')
    def _check_skill_level(self):
        for record in self:
            if record.skill_level_id not in record.skill_type_id.skill_level_ids:
                raise ValidationError(_("The skill level %(level)s is not valid for skill type: %(type)s",
                                        level=record.skill_level_id.name, type=record.skill_type_id.name))


class SkillLevel(models.Model):
    _name = 'res.skill.level'
    _description = "Skill Level"
    _order = "level_progress desc"

    skill_type_id = fields.Many2one('res.skill.type', ondelete='cascade', string='Tipo de Habilidad')
    name = fields.Char(required=True, string='Nivel')
    level_progress = fields.Integer(string="Progreso",
                                    help="Progreso desde cero conocimiento (0%) hasta conocimiento total (100%).")


class SkillType(models.Model):
    _name = 'res.skill.type'
    _description = "Skill Type"

    name = fields.Char(required=True, string='Tipo de Habilidades')
    skill_ids = fields.One2many('res.skill', 'skill_type_id', string="Habilidades")
    skill_level_ids = fields.One2many('res.skill.level', 'skill_type_id', string="Niveles")
