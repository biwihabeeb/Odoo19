# -*- coding: utf-8 -*-
from odoo import api, models, fields


class ExampleLine(models.Model):
    """"""
    _name = 'example.line'
    _description = 'Example Line'

    product_id = fields.Many2one(
        'product.product',
        string='Product'
    )
    quantity = fields.Integer(string='Quantity',default=1)
    price = fields.Float(
        string='Unit Price',
        readonly=False
    )
    sub_total = fields.Float(
        string='Sub Total',
        compute='_compute_sub_total',
        store=True,

    )
    example_id = fields.Many2one('example')

    @api.depends('price','quantity')
    def _compute_sub_total(self):
        for rec in self:
            rec.sub_total = rec.price * rec.quantity

    @api.onchange('product_id')
    def _onchange_product_id(rec):
        if rec.product_id:
            rec.price = rec.product_id.lst_price


    
