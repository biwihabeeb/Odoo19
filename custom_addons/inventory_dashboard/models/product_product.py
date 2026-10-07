# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def get_location_stock(self):
        stock_location = self.search_read(
            [],
            ['name','location_id','warehouse_id'],
        )
        print('STOCK LOCATION')
        for record in stock_location:
            print(record)
        return stock_location