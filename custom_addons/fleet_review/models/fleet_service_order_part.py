# -*- coding: utf-8 -*-

from odoo import fields, models, api

class FleetServiceOrderPart(models.Model):
    _name = 'fleet.service.order.part'
    _rec_name = 'product_id'


    name = fields.Char(
        string='Name',
    )
    order_id = fields.Many2one(
        'fleet.service.order'
    )
    # — Many2one → fleet.service.order
    product_id = fields.Many2one(
        'product.product'
    )
    # — Many2one → product.product
    quantity = fields.Float(
        string="Quantity",
        default=1.0,
    )
    unit_price = fields.Float(
        string="Unit Price",
        readonly=False,
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.lst_price
            self.quantity = 1


