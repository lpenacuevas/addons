import json
import math
import logging
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class visitantes(models.Model):
    _name = 'visitantes'
    _description = 'modelo de visitantes'
    

    _inherit = ["mail.thread", "mail.activity.mixin"]

    _rec_name = "document"
    
    document = fields.Char("Documento")
    visitor = fields.Char("Visitante")
    date = fields.Datetime("Fecha") # TODO: Cambiar a tipo Date y hacer que tome la fecha automaticamente.

    entry_date_time = fields.Datetime(
        "Hora de entrada",
        default=lambda self: fields.Datetime.now()) # TODO: Modificar para que solo muestre la hora.

    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True)

    unit = fields.Char("Unidad")

    floor = fields.Integer("Piso")

    photo = fields.Binary(attachment=False)

    duration = fields.Float('Duration', store=True, compute='_compute_duration', readonly=False)



    # This function set the unit & floor to it's respective fields
    @api.onchange("employee_id")
    def change_fields(self):
        if self.employee_id:
            self.unit = self.employee_id.department_id.name
            self.floor = self.employee_id.department_id.piso_id.numero

    # TODO: Crear una función que extraiga la fecha y la hora del campo create_date y los setee como campos aparte en campos date & hour
    # TODO: Crear una función que calcule la diferencia entra la hora de salida y la hora de entrada.
    # TODO: 


    #Hora de salida (Campo de salida)
    # departure_date_time = fields.Datetime(
    #     "Hora de salida",
    #     default=lambda self: fields.Datetime.now())
    #Time will be a calculated field between departure_date_time - entry_date_time
    
    # invoice_line_ids = fields.One2many('account.move.line', 'move_id', string='Invoice lines',
    #     copy=False, readonly=True,
    #     domain=[('exclude_from_invoice_tab', '=', False)],
    #     states={'draft': [('readonly', False)]})
    

    @api.depends('write_date', 'create_date')
    def _compute_duration(self):
        for event in self:
            event.duration = self._get_duration(event.create_date, event.write_date)
            
    def _get_duration(self, create_date, write_date):
        """ Get the duration value between the 2 given dates. """
        if not create_date or not write_date:
            return 0
        else:
            duration = (write_date - create_date).total_seconds() / 3600
            return duration
        




    # #Consulta a api-----------------------------------------
    # @api.model
    # def using_api_external(self, cedula):
    #     if cedula:
    #         try:
    #             # token = (
    #             #     self.env['ir.config_parameter'].sudo().get_param("api.service_id"))
    #             api_url = (
    #                 self.env['ir.config_parameter'].sudo().get_param('uri') + cedula)               
    #             _logger.warning(api_url)
    #             response = requests.get(api_url,
    #                                     headers={
    #                                         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2'
    #                                         #    "XApiKey": token
    #                                     })
    #         except requests.exceptions.ConnectionError as e:
    #             _logger.warning(
    #                 "API request return the following error %s" % e)
    #             return {"status": "error", "data": []}
    #         try:               
    #             # data = self.convertXmlToJson(response.content)
    #             return json.loads(response.content)
    #         except TypeError:
    #             _logger.warning("No serializable data from api response")
    #     return False

    # Pasa valores a los campos
    # @api.model
    # def passing_data(self, number):
    #     result = {}
    #     partner_json = self.using_api_external(number)
    #     if partner_json:
    #         data = dict(partner_json) 
    #         _logger.warning(data['citizenInfo'])
                       
    #         result["name"] = ''
    #     return result
 
    # Actualiza los campos
    # def _get_updated_vals(self, vals):
    #     new_vals = {}
    #     if any([val in vals for val in ["name", "name"]]):
    #         vat = vals["name"] if vals.get("vat") else vals.get("name")
    #         result = self.with_context(model=self._name).passing_data(vat)
    #         if result is not None:
    #             if "name" in result:
    #                 new_vals["name"] = result.get("name")
    #     return new_vals

    # @api.model_create_multi
    # def create(self, values):
    #     for vals in values:
    #         vals.update(self._get_updated_vals(vals))
    #     return super(visitantes, self).create(values)

    
    # def convertXmlToJson(self, value):
    #     xml_dict = {}
    #     root = ET.fromstring(value)
    #     for elem in root:
    #         xml_dict[elem.tag] = elem.text
    #     return json.dumps(xml_dict, indent=4)
