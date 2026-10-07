# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    activate_purchase_limit = fields.Boolean(
        string="Activate Purchase Limit",
        default=False,
    )

    purchase_limit_amount = fields.Float(
        string="Purchase Amount Cap",
    )

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['activate_purchase_limit', 'purchase_limit_amount']
        print('DATA: ', data)
        return data