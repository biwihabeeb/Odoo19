# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    restricted_combo_ids = fields.Many2many(
        'product.product',
        relation='product_restricted_product_combo_rel',
        column1= 'product_id',
        column2= 'restricted_id',
        # domain= [('id', 'not in','restricted_combo_ids')]
    )