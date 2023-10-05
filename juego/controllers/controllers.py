# -*- coding: utf-8 -*-
# from odoo import http


# class Juego(http.Controller):
#     @http.route('/juego/juego', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/juego/juego/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('juego.listing', {
#             'root': '/juego/juego',
#             'objects': http.request.env['juego.juego'].search([]),
#         })

#     @http.route('/juego/juego/objects/<model("juego.juego"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('juego.object', {
#             'object': obj
#         })
