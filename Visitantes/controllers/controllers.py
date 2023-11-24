# -*- coding: utf-8 -*-
# from odoo import http


# class Localidad(http.Controller):
#     @http.route('/localidad/localidad', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/localidad/localidad/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('localidad.listing', {
#             'root': '/localidad/localidad',
#             'objects': http.request.env['localidad.localidad'].search([]),
#         })

#     @http.route('/localidad/localidad/objects/<model("localidad.localidad"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('localidad.object', {
#             'object': obj
#         })
