# -*- coding: utf-8 -*-
from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        location = self.env["stock.location"].search([('name','=','Heavy Rack')])
        for rec in self.move_ids:
            print(rec.product_id.weight)
            if rec.product_id.weight > 20:
                self.write({
                    'location_dest_id': location.id,
                })
        print('validate!')
        return super().button_validate()


