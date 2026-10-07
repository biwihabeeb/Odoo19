# -*- coding: utf-8 -*-

from odoo import fields,models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    associated_customer_id = fields.Many2one(
        comodel_name='res.partner',
    )