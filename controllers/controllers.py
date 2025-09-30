# -*- coding: utf-8 -*-
# from odoo import http


# class Immatriculation(http.Controller):
#     @http.route('/immatriculation/immatriculation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/immatriculation/immatriculation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('immatriculation.listing', {
#             'root': '/immatriculation/immatriculation',
#             'objects': http.request.env['immatriculation.immatriculation'].search([]),
#         })

#     @http.route('/immatriculation/immatriculation/objects/<model("immatriculation.immatriculation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('immatriculation.object', {
#             'object': obj
#         })

