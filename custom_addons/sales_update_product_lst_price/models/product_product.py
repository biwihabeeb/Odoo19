# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    # price_update_id = fields.Many2one(
    #     'bulk.price.update'
    # )