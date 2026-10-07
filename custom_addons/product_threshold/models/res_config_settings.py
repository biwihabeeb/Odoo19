# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_threshold = fields.Float(
        string="Product Threshold",
        config_parameter='product_threshold.product_threshold',
    )