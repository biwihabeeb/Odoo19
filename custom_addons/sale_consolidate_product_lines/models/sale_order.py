# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_consolidate_duplicate_product_line(self):
        product_ids = []
        duplicates = {}
        for rec in self.order_line:
            if rec.product_id in product_ids:
                duplicates[rec.product_id] += rec.product_uom_qty
            else:
                product_ids.append(rec.product_id)
                duplicates.update({rec.product_id: rec.product_uom_qty})

        self.update({
            'order_line': [
                fields.Command.clear()
            ]
        })
        self.update({
            'order_line': [
                fields.Command.create({
                    'product_id': key.id,
                    'product_uom_qty': duplicates[key],
                }) for key in duplicates
            ]
        })
        print(duplicates)

