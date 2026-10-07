# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_brand = fields.Char(
        string="Product Brand"
    )

    product_master_type = fields.Selection(
        selection=[
            ('single', 'Single Product'),
            ('brand', 'Branded Product'),
        ]
    )