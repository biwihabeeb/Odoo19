# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'


    associated_product_ids = fields.Many2many(
        'product.product',
        relation='product_product_product_product_rel',
        column1='product_id',
        column2='associated_product_id',
        string='Associated Products ',
    )
