# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def get_max_total_amount_so_partner(self):
        data = self.search_read([], fields=['partner_id','name','amount_total'], order='amount_total desc', limit=1)
        return data