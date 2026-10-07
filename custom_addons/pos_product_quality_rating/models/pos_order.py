# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    quality_rating = fields.Selection(
        related='product_id.quality_rating',
    )

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data.append('quality_rating')
        return data