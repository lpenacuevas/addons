# -*- coding: utf-8 -*-
# from odoo import http


# class DepartamentoLocalidad(http.Controller):
#     @http.route('/departamento_localidad/departamento_localidad', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/departamento_localidad/departamento_localidad/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('departamento_localidad.listing', {
#             'root': '/departamento_localidad/departamento_localidad',
#             'objects': http.request.env['departamento_localidad.departamento_localidad'].search([]),
#         })

#     @http.route('/departamento_localidad/departamento_localidad/objects/<model("departamento_localidad.departamento_localidad"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('departamento_localidad.object', {
#             'object': obj
#         })
