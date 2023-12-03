import json
import math
import logging
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class tags_visitantes(models.Model):
    _name = 'tags.visitante'
    _description = 'tags de visitantes'

    name = fields.Char("detalles")
    sequence = fields.Integer('Secuencia',default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default=True)
    color = fields.Integer("Índice de Colores")