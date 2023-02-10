# -*- coding: utf-8 -*-
# from odoo import http


# class WhiteClover(http.Controller):
#     @http.route('/white_clover/white_clover', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/white_clover/white_clover/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('white_clover.listing', {
#             'root': '/white_clover/white_clover',
#             'objects': http.request.env['white_clover.white_clover'].search([]),
#         })

#     @http.route('/white_clover/white_clover/objects/<model("white_clover.white_clover"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('white_clover.object', {
#             'object': obj
#         })
