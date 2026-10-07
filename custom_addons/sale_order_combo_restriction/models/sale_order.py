# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        # print(self.order_line.mapped('product_id').restricted_combo_ids)
        restricted_combo_product_ids = self.order_line.mapped('product_id').restricted_combo_ids
        for line in self.order_line:
            print('product_id', line.product_id.id, restricted_combo_product_ids.ids)
            if line.product_id.id in restricted_combo_product_ids.ids:
                print(line.product_id)
                raise ValidationError("Order line contains restricted combination(s) of products")
        return super().action_confirm()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    restricted_product_ids = fields.Many2many(
        'product.product',
        related='product_id.restricted_combo_ids'
    )