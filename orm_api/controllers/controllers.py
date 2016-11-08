# -*- coding: utf-8 -*-
from openerp import http

# class OrmApi(http.Controller):
#     @http.route('/orm_api/orm_api/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/orm_api/orm_api/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('orm_api.listing', {
#             'root': '/orm_api/orm_api',
#             'objects': http.request.env['orm_api.orm_api'].search([]),
#         })

#     @http.route('/orm_api/orm_api/objects/<model("orm_api.orm_api"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('orm_api.object', {
#             'object': obj
#         })
