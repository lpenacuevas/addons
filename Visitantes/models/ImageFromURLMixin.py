from odoo import api, fields, models
import requests
import logging
import base64

_logger = logging.getLogger(__name__)

class ImageFromURLMixin:
   def get_image_from_url(self, url):
       """
       :return: Returns a base64 encoded string.
       """
       data = ""
       try:
        #    image = f"data:image/jpg;base64,{}"
           data = url.strip()
       except Exception as e:
           _logger.warning("Can’t load the image from URL %s" % url)
           logging.exception(e)
       return data