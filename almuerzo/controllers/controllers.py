# -*- coding: utf-8 -*-
# from odoo import http


# class Almuerzo(http.Controller):
#     @http.route('/almuerzo/almuerzo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almuerzo/almuerzo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('almuerzo.listing', {
#             'root': '/almuerzo/almuerzo',
#             'objects': http.request.env['almuerzo.almuerzo'].search([]),
#         })

#     @http.route('/almuerzo/almuerzo/objects/<model("almuerzo.almuerzo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almuerzo.object', {
#             'object': obj
#         })
