# -*- coding: utf-8 -*-
from odoo import api, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    # @api.model
    # def get_stock_location(self):
    #     query = """
    #     select
    #         l.complete_name,
    #         sum(q.quantity),
    #         q.in_date
    #     from
    #         stock_quant q
    #     inner join
    #         stock_location l on l.id = q.location_id
    #     group by l.complete_name,q.in_date;
    #     """
    #     self.env.cr.execute(query)
    #     stock_location = self.env.cr.dictfetchall()
    #     print('STOCK LOCATION')
    #     for record in stock_location:
    #         print(record)
    #     return stock_location

    # @api.model
    # def get_inventory_valuation(self):