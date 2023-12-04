import json
import math
import logging
import requests
import base64
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from odoo import models, fields, api
from .ImageFromURLMixin import ImageFromURLMixin
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class visitante(models.Model,ImageFromURLMixin):
    _name = 'visitante'
    _description = 'modelo de visitantes'
    _rec_name = 'first_name'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    name = fields.Char("Cedula")
    first_name = fields.Char("Nombre")
    last_name = fields.Char("Apellido")  
    photo = fields.Binary("Image")

    line_ids = fields.One2many(
        'visitante.line',
        'visitante_id',
         string="Empleados con visitas")  

    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado'
        )

    departments_id = fields.Many2one(
        'hr.department',
        string="Departamento",
        readonly=True
    )

    piso_id = fields.Many2one('localidad.piso',
    string="Piso",
    readonly=True)

    duration = fields.Float('Duration', store=True, compute='_compute_duration', readonly=False)
    color = fields.Integer("Índice de Colores", related="state.color")

    @api.model    
    def _default_state(self):
        default_state = self.env['tags.visitante'].search([('name', '=', 'Entrada')], limit=1)
        return default_state if default_state else False

    state = fields.Many2many(
        "tags.visitante",
        default=_default_state
        )   
    
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
    

    #Consulta a api-----------------------------------------
    @api.model
    def using_api_external(self, cedula):
        if cedula:
            try:
                # token = (
                #     self.env['ir.config_parameter'].sudo().get_param("api.service_id"))
                api_url = (
                    self.env['ir.config_parameter'].sudo().get_param('uri') + cedula)               
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
    
    @api.model
    def convert_image(self, img_uri):        
            image = None
            if img_uri:
                image = self.get_image_from_url(img_uri)
                # self.check_access_rule()                
            return image

    # Pasa valores a los campos
    @api.model
    def passing_data(self, number):
        result = {}
        partner_json = self.using_api_external(number)
        if partner_json:
            data = dict(partner_json) 
            citizen = data["citizenInfo"]
            result["first_name"] = citizen['nombres']
            result["last_name"] = f"{citizen['apellido1']} {citizen['apellido2']}"
            result["photo"] = self.convert_image(citizen['foto_encoded'])
            _logger.warning(result['photo'])      
        return result

    @api.model
    def passing_data_contact(self, number):
        result = self.env['res.partner'].search([('vat', '=', number)], limit=1)  
        return result

    # Actualiza los campos
    def _get_updated_vals(self, vals):
        new_vals = {}
        if any([val in vals for val in ["name", "name"]]):
            vat = vals["name"] if vals.get("vat") else vals.get("name")   
            partner = self.with_context(model=self._name).passing_data_contact(vat)            
            if partner:
                for contact in partner:                                    
                    new_vals["first_name"] = contact.name
                    
            else:    
                result = self.with_context(model=self._name).passing_data(vat)                        
                if result is not None:
                    self.env['res.partner'].create({
                    'name': result["first_name"],
                    'vat': vat,
                    'image_1920': result["photo"]
                    })
                    if "first_name" in result:
                        new_vals["first_name"] = result["first_name"]
                    if "last_name" in result:
                        new_vals["last_name"] = result["last_name"]
                    if "photo" in result: 
                        new_vals['photo'] = result["photo"]           
        return new_vals

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            vals.update(self._get_updated_vals(vals))
        return super(visitante, self).create(values)

    @api.onchange('employee_id')
    def _change_field(self):
        for record in self:
            if record.employee_id:
                record.piso_id = record.employee_id.department_id.piso_id.id
                record.departments_id = record.employee_id.department_id.id
    
    
  