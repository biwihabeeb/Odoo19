# -*- coding: utf-8 -*-
from odoo import api, models

class StockLocation(models.Model):
    _inherit = 'stock.location'

    @api.model
    def get_stock_location(self, filter):
        query = """
        select 
            sum(q.quantity) as quantity, 
            l.complete_name as location 
        from 
            stock_quant q 
        inner join 
            stock_location l 
        on 
            l.id = q.location_id
        group by 
            l.complete_name;
        """

        self.env.cr.execute(query)
        stock_location = self.env.cr.dictfetchall()
        # print('STOCK_LOCATION')
        #
        # for quant in stock_location:
        #     print(quant)
        # for rec in stock_location:
        #     for quant in rec['quant_ids']:
        #         print(self.env['stock.quant'].browse(quant).search_read([],['product_id','quantity']))
        return stock_location