from odoo import models, fields, api

class custom_hr_resume_line(models.Model):
    _inherit = "hr.resume.line"

    cargo = fields.Char("Cargo")

    tipo_institucion =  fields.Selection(
        [("INSTITUCIÓN PÚBLICA","INSTITUCIÓN PÚBLICA"),
         ("EMPRESA PRIVADA","EMPRESA PRIVADA"),
         ("INSTITUCIÓN ACADÉMICA","INSTITUCIÓN ACADÉMICA"),
         ("OTHER", "OTHER")],
        "Tipo De Empresa")

    telefono = fields.Char("Telefono") 