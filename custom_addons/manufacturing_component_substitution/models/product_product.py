# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'


    alternate_component_ids = fields.Many2many(
        'product.product',
        relation='product_component_alternate_component_rel',
        column1='component_id',
        column2='alternate_component_id',
        string='Alternate Components',

    )
    alternate_component_id = fields.Many2one(
        'product.product',
        string='Alternate Component',
    )

    @api.onchange('product_brand')
    def onchange_product_brand(self):
        print('BRAND>>')
        if self.product_brand:
            self.name = self.name + " (" + self.product_brand + ")"
        else:
            self.name = self.name
