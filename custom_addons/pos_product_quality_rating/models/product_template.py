# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    quality_rating = fields.Selection(
        [
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
        ],
        string='Quality Rating',
    )

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['quality_rating']
        return data