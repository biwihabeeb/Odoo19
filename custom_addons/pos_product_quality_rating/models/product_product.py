    # -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    quality_rating = fields.Selection(
        related='product_tmpl_id.quality_rating',
        string='Quality Rating',
    )

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['quality_rating']
        # print(data)
        return data