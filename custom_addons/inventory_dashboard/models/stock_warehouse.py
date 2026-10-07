# -*- coding: utf-8 -*-
from odoo import api, models

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    @api.model
    def get_warehouse_locations(self, filter):
        query = f"""
        select 
	        w.name as warehouse, 
	        l.complete_name as location
        from 
	        stock_warehouse w 
        inner join 
	        stock_location l 
        on 
	        l.id = w.wh_input_stock_loc_id 
        or 	
	        l.id = w.wh_qc_stock_loc_id
        or
	        l.id = w.wh_output_stock_loc_id
        or
	        l.id = w.wh_pack_stock_loc_id
	    where
	        l.company_id = {self.env.company.id};
        """
        self.env.cr.execute(query)
        wh_locations = self.env.cr.dictfetchall()
        # print(wh_locations)
        return wh_locations