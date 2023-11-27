from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class custom_hr_applicant(models.Model):
    _inherit = "hr.applicant"

    partner_name = fields.Many2one(
        comodel_name='res.partner',
        string=' Nombre del candidato',
        domain="[('is_applicant','=', True)]",
        required=True
    )

    @api.onchange('job_id')
    def _compute_name_job(self):
        for rec in self:
            rec.name = rec.job_id.name

    is_created = fields.Boolean(
        string='Se Creo una accion')

    def open_wizar(self):
        action_type_lower = self.env['action.type'].search([('name', '=', 'INGRESO')])
        if action_type_lower:
            action_type_lower.name.lower()
        else:
            raise UserError('La accion de tipo "Ingreso" aun no ha sido creada')
        if self.is_created == True:
            raise UserError('La novedad ya ha sido creada anteriormente')
        return {
            'name': 'Novedades',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.custom',
            'view_mode': "form",
            'target': 'new',
            'context': {
                'default_action_type_id': action_type_lower.id,
                'default_applicant_id': self.partner_name.id,
                'default_departments_id': self.department_id.id,
                'default_position_id': self.job_id.id
            }
        }

    # 'name': Puedes agregar un nombre descriptivo a la acción que se mostrará en la interfaz de usuario.

    # 'domain': Permite filtrar los registros que se mostrarán en la ventana emergente en función de ciertos criterios.

    # 'context': Puedes pasar un contexto personalizado que se utilizará al abrir la ventana emergente. Esto puede incluir valores predeterminados, variables o cualquier otro dato que desees utilizar en la acción.

    # 'res_id': Si deseas abrir una ventana emergente con un registro específico, puedes proporcionar su ID en res_id.

    # 'views': Puedes especificar diferentes modos de vista (por ejemplo, vista de lista, vista de árbol, vista de formulario) en la ventana emergente y personalizar la presentación de los datos.

    # 'search_view_id': Define una vista de búsqueda personalizada para la acción.

    # 'search_view_id': Puedes especificar una vista personalizada para la búsqueda en la acción.

    # 'src_model': Si estás realizando una acción desde un modelo diferente, puedes especificar el modelo de origen.

    # 'view_id': Define una vista personalizada que se utilizará en lugar de la vista predeterminada.

    # 'view_ids': Especifica una lista de vistas que se utilizarán en la acción.
