import json
import logging
import requests
import xml.etree.ElementTree as ET

from odoo import models, fields, api
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class visitantes(models.Model):
    _name = 'visitantes'
    _description = 'modelo de visitantes'

    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    
    name = fields.Char("Cedula")
    
    
    # Consulta a api
    @api.model
    def using_api_external(self, cedula):
        if cedula:
            try:
                # token = (
                #     self.env['ir.config_parameter'].sudo().get_param("api.service_id"))
                api_url = (
                    self.env['ir.config_parameter'].sudo().get_param('uri') + cedula)               
                _logger.warning(api_url)
                response = requests.get(api_url,
                                        headers={
                                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2'
                                            #    "XApiKey": token
                                        })
            except requests.exceptions.ConnectionError as e:
                _logger.warning(
                    "API request return the following error %s" % e)
                return {"status": "error", "data": []}
            try:               
                # data = self.convertXmlToJson(response.content)
                return json.loads(response.content)
            except TypeError:
                _logger.warning("No serializable data from api response")
        return False

    # Pasa valores a campos
    @api.model
    def passing_data(self, number):
        result = {}
        partner_json = self.using_api_external(number)
        if partner_json:
            data = dict(partner_json) 
            _logger.warning(data['citizenInfo'])
                       
            # result["name"] = ''
        return result

    # Actualiza los campos
    def _get_updated_vals(self, vals):
        new_vals = {}
        if any([val in vals for val in ["name", "name"]]):
            vat = vals["name"] if vals.get("vat") else vals.get("name")
            result = self.with_context(model=self._name).passing_data(vat)
            if result is not None:
                if "name" in result:
                    new_vals["name"] = result.get("name")
        return new_vals

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            vals.update(self._get_updated_vals(vals))
        return super(visitantes, self).create(values)


    
    # def convertXmlToJson(self, value):
    #     xml_dict = {}
    #     root = ET.fromstring(value)
    #     for elem in root:
    #         xml_dict[elem.tag] = elem.text
    #     return json.dumps(xml_dict, indent=4)
