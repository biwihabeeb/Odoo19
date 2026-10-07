# -*- coding: utf-8 -*-
from odoo import fields, models, api

class UpdatedPriceSummary(models.TransientModel):
    _name = 'updated.price.summary'

    updated_product_ids = fields.Many2many(
        'price.update.line',
        readonly=True,
    )

    update_id = fields.Many2one(
        'bulk.price.update'
    )