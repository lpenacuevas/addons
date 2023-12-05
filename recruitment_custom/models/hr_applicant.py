from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class custom_hr_applicant(models.Model):
    _inherit = "hr.applicant"

    partner_name = fields.Many2one(
        comodel_name='partner.applicant',
        string=' Nombre del candidato',
        required=True
    )

    employee_id = fields.Many2one('hr.employee', 'Empleado responsable')

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

    # poor = fields.Boolean(string='Deficiente')
    # normal = fields.Boolean(string='Regular')
    # good = fields.Boolean(string='Bueno')
    # better = fields.Boolean(string='Muy bueno')
    # excellent = fields.Boolean(string='Excenlente')

    education_level = fields.Selection(
        string='Nivel Educacional (Requerido según descripción del cargo)',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    experience_level = fields.Selection(
        string='Experiencia de Trabajo (Según descripción del Cargo y Requerida)',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    behavior_level = fields.Selection(
        string='Actitud en la Entrevista (seguridad, lenguaje )',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    job_level = fields.Selection(
        string='Estabilidad Laboral',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    working_level = fields.Selection(
        string='Disposición al Trabajo',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    personal_relationship_level = fields.Selection(
        string='Relaciones Interpersonales',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    goals_level = fields.Selection(
        string='Comprensión de Metas y Objetivos',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])

    learning_level = fields.Selection(
        string='Rapidez para entender Conceptos',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    assistance_level = fields.Selection(
        string='Asistencia Puntual',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    talking_level = fields.Selection(
        string='Fluidez Verbal',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    personal_appearance_level = fields.Selection(
        string='Apariencia personal para el puesto vacante',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    ideas_coordination_level = fields.Selection(
        string='Coordinación de Ideas',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    improving_level = fields.Selection(
        string='Potencial de Desarrollo',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])
    expectations_level = fields.Selection(
        string='Expectativas Laborales',
        selection=[('poor', 'Deficiente'),
                   ('normal', 'Regular'),
                   ('good', 'Bueno'),
                   ('better', 'Muy bueno'),
                   ('excellent', 'Excelente')])

    currently_working = fields.Selection(
        string='Labora en la actualidad:',
        selection=[('yes', 'Si'),
                   ('no', 'No')])

    actual_past_job = fields.Char('Nombre Actual/Ultima:', store=True)
    actual_past_position = fields.Char('Posición actual/Última:', store=True)
    actual_past_salary = fields.Char('Salario Actual/Último:', store=True)
    actual_past_from = fields.Char('Desde', store=True)
    actual_past_to = fields.Char('Hasta', store=True)

    leaving_last_job_reason = fields.Char('Razón de salida trabajo actual o último:')
    salary_expectation = fields.Char('Expectativa salarial:')
    time_availability = fields.Char('Disponibilidad de tiempo:')
    applicant_strengths = fields.Char('Fortalezas del candidato(a):')
    improvement_opportunities = fields.Char('Oportunidades de mejora:')

    competencies = fields.Char('Competencias')
    another_job_position = fields.Char('Considerar para otro Puesto:')
    unselected = fields.Char('No considerar:')

    """---------------------------Section: Fields for check list---------------------------------- """
    map_document = fields.Selection(
        string='Respuesta de No Objeción del Map',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    staff_action = fields.Selection(
        string='Acción de Personal',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    appointment_def = fields.Selection(
        string='Nombramiento Definitivo',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    appointment_temp = fields.Selection(
        string='Nombramiento Temporal',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    offer_letter = fields.Selection(
        string='Carta Oferta Laboral',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    supervisor_notf = fields.Selection(
        string='Copia Notificación de ingreso al Supervisor Inmediato',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    partner_identification = fields.Selection(
        string='Copia de Cédula del(a) canditato(a)',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    general_information = fields.Selection(
        string='Formulario de Datos Generales',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    partner_resume = fields.Selection(
        string='Curriculim Vítae',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    partner_academy_information = fields.Selection(
        string='Copia de Títulos Académicos y/o Certificados de estudios',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    exequatur_copy = fields.Selection(
        string='Copia de exequátur',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    license_copy = fields.Selection(
        string='Copia de la Licencia',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    bank_account = fields.Selection(
        string='Evidencia Cuenta de Banco Reservas',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    account_match = fields.Selection(
        string='Verificación cruce de Nóminas Contraria',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    last_institution = fields.Selection(
        string='Certificación de Laboró Institución Anterior',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    background_certification = fields.Selection(
        string='Certificación de Buena Conducta',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    medical_record = fields.Selection(
        string='Resultados Analisis Médicos',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    medical_evalutation = fields.Selection(
        string='Evaluación Médica Pre-empleo',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    confidential_agreement = fields.Selection(
        string='Acuerdo de confidencialidad',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    interest_conflict = fields.Selection(
        string='Formulario Declaración de Conflictos de Interes',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    bagde_form = fields.Selection(
        string='Formulario de Carnet y Acuse de recibido',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    internal_induction = fields.Selection(
        string='Acuse de Inducción',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])
    mitur_ethic = fields.Selection(
        string='Declaración de conocimiento y compromiso de cumplimiento del Códifo de Ética MITUR',
        selection=[('Si', 'Si'),
                   ('No', 'No'),
                   ('N/A', 'N/A')])

    """------------------------End Section: Fields for check list------------------------------ """

    @api.onchange('partner_name')
    def _compute_fields_from_partner(self):
        for rec in self:
            partner_job = rec.partner_name.partner_job_ids.filtered(
                lambda record: record.id == rec.partner_name.partner_job_ids[0].id)
            if partner_job:
                rec.actual_past_job = partner_job.name
                rec.actual_past_position = partner_job.job_position
                rec.actual_past_salary = partner_job.salary
                rec.actual_past_from = partner_job.enter_date
                rec.actual_past_to = partner_job.end_date


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
