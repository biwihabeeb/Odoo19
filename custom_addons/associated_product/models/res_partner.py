# -*- coding: utf-8 -*-

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    associated_products_ids = fields.Many2many(
        comodel_name='product.product',
        string='Associated Products',
        relation='res_partner_product_product_rel'
    )


