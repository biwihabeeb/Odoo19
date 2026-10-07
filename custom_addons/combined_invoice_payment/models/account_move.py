# -*- coding: utf-8 -*-
from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    currency_id = fields.Many2one(
        'res.currency',
    )
    custom_amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        store=True,
    )




