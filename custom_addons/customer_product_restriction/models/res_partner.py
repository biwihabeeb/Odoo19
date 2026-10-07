# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    allowed_product_ids = fields.Many2many(
        'product.product',
        string='Allowed Products',
        relation='res_partner_allowed_products_rel'
        # column1='partner_id',
        # column2='allowed_product_id',
    )

    order_limit = fields.Integer(
        string='Order Line Limit',
        default=3,
    )