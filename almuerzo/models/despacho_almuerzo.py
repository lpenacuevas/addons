from datetime import datetime
import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class almuerzo_comida(models.Model):
    _name = 'almuerzo.despacho.almuerzo'
    _description = 'Modelo de despacho de almuerzo'
    
    cedula = fields.Char("Cédula")
    first_name = fields.Char("Nombre")
    last_name = fields.Char("Apellidos")
    name = fields.Char("Nombre completo", readonly=True)
    unit = fields.Char("Unidad", readonly=True)
    tipo_persona_almuerza = fields.Many2one("almuerzo.almuerzo")
    contact_object = fields.Many2one("almuerzo.almuerzo")

    @api.onchange("cedula")
    def update_lunch_parameters(self):

        for rec in self:
            """
            Update lunch parameters based on the identification number provided.

            This method is triggered whenever the identification number field is changed. It removes dashes from
            the identification number, searches for an employee and the most recent lunch record associated with the
            identification number, and updates the lunch parameters accordingly.

            If an employee is allowed to eat, the method sets the first name, last name, unit, and triggers the
            notification for successful access. If the identification number does not match any records or the person
            is not allowed to eat, a warning is logged, and a validation error is raised.

            If the person is a contact allowed to eat, the method sets the first name, last name, contact object,
            unit, and triggers the notification for successful access.

            :return: None
            :raises: ValidationError if the identification number is not found or the person is not allowed to eat.
            """

            if not rec.cedula:
                return

            # Remove dashes from the identification number
            formatted_cedula = rec.cedula.replace('-', '')
            rec.cedula = formatted_cedula

            # Search for an employee and the most recent lunch record associated with the identification number
            employee_obj = self.env['hr.employee'].search([('identification_id', '=', formatted_cedula), ('identification_id', '!=', '')], limit=1)
            contact_records = self.env['almuerzo.almuerzo'].search([('cedula', '=', formatted_cedula)])
            contact_obj = contact_records.sorted(key=lambda r: r.create_date, reverse=True)[0] if contact_records else None
            
            if formatted_cedula:
                # Check if the employee is allowed to eat
                employee_is_allowed_to_eat = True if employee_obj and employee_obj.enter_date and ((not employee_obj.end_date) or (employee_obj.end_date and datetime.now().date() <= employee_obj.end_date)) else False
                contact_is_allowed_to_eat = True if contact_obj and datetime.now().date() >= contact_obj.from_date and datetime.now().date() <= contact_obj.date_to else False

                # Handle cases based on whether the person is an employee or contact allowed to eat
                if not (employee_is_allowed_to_eat or contact_is_allowed_to_eat):
                    raise ValidationError("Cédula no encontrada. Por favor, ingrese una cédula válida o póngase en contacto con el administrador del sistema.")

                if employee_is_allowed_to_eat:
                    rec.first_name = employee_obj.name
                    rec.last_name = employee_obj.last_name
                    rec.unit = employee_obj.department_id.name
                    self._compute_full_name()
                elif contact_is_allowed_to_eat:
                    rec.first_name = contact_obj.first_name
                    rec.last_name = contact_obj.last_name
                    rec.contact_object = contact_obj.id
                    rec.unit = contact_obj.unit.name
                    self._compute_full_name()


    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        """Set full name throughout the name field"""
        for rec in self:
            rec.name = f"{self.first_name} {self.last_name}"
            return rec.name

    # Working on this
    # def send_notification(self, notification_type):
    #     """ Send a non-sticky notification that disappears from the screen a few seconds after being triggered
    #         based on the provided notification type.

    #         The method checks whether the notification type is 'success' or 'danger' and constructs a notification
    #         with a title and message accordingly. Success notifications have a default title of 'Access Allowed',
    #         while danger notifications have a title of 'Access Denied'. The notifications are of non-sticky type,
    #         meaning they disappear from the screen after a short duration.

    #         :param notification_type: A string indicating the type of notification, either 'success' or 'danger'.
    #         :return: A dictionary representing the notification configuration.
    #     """
    #     if notification_type not in ['success', 'danger']:
    #         raise ValueError("Invalid notification type. Supported types: 'success', 'danger'")

    #     notification = {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification',
    #         'params': {
    #             'title': ('ACCESO PERMITIDO'),
    #             'message': 'ACCESO PERMITIDO',
    #             'type':'success',  #types: success,warning,danger,info
    #             'sticky': True,  #True/False will display for few seconds if false
    #         },
    #     }

    #     if notification_type == 'success':
    #         return notification
    #     elif notification_type == 'danger':
    #         notification['params']['title'] = 'ACCESO DENEGADO'
    #         notification['params']['message'] = 'DENEGADO'
    #         notification['params']['type'] = notification_type
    #         return notification

#TODO: Crear alerta de acceso permitido (Verde) o denegado (Roja). Si es denegado debe de lanzar una excepcion.
