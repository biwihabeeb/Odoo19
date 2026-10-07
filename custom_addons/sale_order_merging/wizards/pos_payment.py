# -*- coding: utf-8 -*-
from odoo import fields, models

class PosPayment(models.TransientModel):
    _name = 'pos.payment'

    sale_id = fields.Many2one(
        'sale.order'
    )
    payment_id = fields.Many2one(
        'pos.payment.method'
    )

    payment_line_ids = fields.One2many(
        'pos.payment.line',
    )


class PosPaymentLine(models.TransientModel):
    _name = 'pos.payment.line'


