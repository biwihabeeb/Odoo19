# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    add_mandatory_products = fields.Boolean(
        string="Add Mandatory Products",
        config_parameter="mandatory_products.add_mandatory_products",
    )