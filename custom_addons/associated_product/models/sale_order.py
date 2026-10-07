# -*- coding: utf-8 -*-
from os import unlink

from odoo import api,fields,models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    add_associated_products = fields.Boolean(
        string='Add Associated Products?'
    )

    @api.onchange('add_associated_products','partner_id')
    def onchange_add_associated_products(self):
        if self.partner_id and self.add_associated_products:
            self.update({
                'order_line': [
                    fields.Command.create({
                        'product_id': line.id,
                        'price_unit': line.lst_price,
                        'product_uom_qty': 1
                    }) for line in self.partner_id.associated_products_ids
                ]
            })

        else:
            for line in self.order_line:
                print(line.id)
            associated_products = self.partner_id.associated_products_ids.ids
            delete_lines = self.order_line.filtered(lambda line: line.product_id.id in associated_products)
            self.update({
                'order_line': [
                    fields.Command.delete(line.id) for line in  delete_lines
                ]
            })



