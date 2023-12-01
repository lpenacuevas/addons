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

    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True)

    unit = fields.Char("Unidad")

    floor = fields.Integer("Piso")

    photo = fields.Binary(attachment=False)

    duration = fields.Float('Duration', store=True, compute='_compute_duration', readonly=False)



    # This function set the unit & floor to it's respective fields
    @api.onchange("employee_id")
    def change_fields(self):
        """
        Update fields based on the selected employee.

        This method is triggered automatically when the "employee_id" field changes.
        It checks if the "employee_id" has a value and updates the "unit" and "floor" fields
        based on the corresponding department information of the selected employee.

        Parameters:
        - self (Recordset): The current recordset.

        Returns:
        None
        """
        if self.employee_id:
            self.unit = self.employee_id.department_id.name
            self.floor = self.employee_id.department_id.piso_id.numero   

    @api.depends('write_date', 'create_date')
    def _compute_duration(self):
        """
        Calculate the duration between 'create_date' and 'write_date' fields using the '_get_duration' function.

        This method is a decorator-dependent function that triggers computation when either 'write_date' or 'create_date' changes.
        It iterates through each record and sets the 'duration' field based on the result of the '_get_duration' function.

        Parameters:
        - self (Recordset): The current recordset.

        Returns:
        None
        """
        for event in self:
            event.duration = self._get_duration(event.create_date, event.write_date)
    
    def _get_duration(self, create_date, write_date):
        """
        Calculate the duration in hours between 'create_date' and 'write_date'.

        Parameters:
        - self (Recordset): The current recordset.
        - create_date (datetime): The date of creation.
        - write_date (datetime): The date of the last write/update.

        Returns:
        float: The duration in hours.
        """
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
