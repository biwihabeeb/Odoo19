# -*- coding: utf-8 -*-

from odoo import fields, api, models


class PriceUpdateLine(models.TransientModel):
    _name = "price.update.line"

    price_update_id = fields.Many2one(
        comodel_name="bulk.price.update"
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
    )
    current_price = fields.Float(
        string="Current Price",

    )

    new_price = fields.Float(
        string="New Price",
        compute="_compute_new_price",
    )

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            self.current_price = self.product_id.lst_price

    @api.depends("price_update_id.update_value","current_price")
    def _compute_new_price(self):
        for rec in self:
            if rec.price_update_id.update_value:
                print('self',rec.current_price)
                if rec.price_update_id.price_update_method == 'fixed':
                    rec.new_price = rec.current_price + rec.price_update_id.update_value
                elif rec.price_update_id.price_update_method == 'percent_increase':
                    rec.new_price = rec.current_price * (1 + 0.01 * rec.price_update_id.update_value)
                else:
                    rec.new_price = rec.current_price * (1 - 0.01 * rec.price_update_id.update_value)
            else:
                rec.new_price = rec.current_price