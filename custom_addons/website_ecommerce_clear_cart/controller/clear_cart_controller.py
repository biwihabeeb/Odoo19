# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class ClearCartController(http.Controller):
    @http.route(['/shop/clear_cart'], type='http', auth="public", website=True, methods=['GET','POST'],csrf=False)
    def clear_cart(self, **kw):
        current_order = request.cart
        print('CURRENT: ',current_order)
        if current_order:
            current_order.unlink()

        return request.redirect('/shop/cart')

