# -*- coding: utf-8 -*-
from openpyxl.worksheet import related

from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    checkout_id = fields.Many2one(
        'library.checkouts'
    )

    invoice_lines_ids = fields.One2many(
        related="checkout_id.checkout_lines_ids"
    )

    book_price = fields.Monetary(
        related="invoice_lines_ids.book_id.book_price"
    )

    penalty_amount = fields.Float(
        related="checkout_id.checkout_penalty"
    )

    def write(self, vals):
        """
        Set status of borrowed book to available, once the invoice is paid
        """
        res = super().write(vals)
        for rec in self:
            if rec.status_in_payment == 'paid' and rec.checkout_id:
                rec.invoice_lines_ids.mapped('book_id').write({
                    'book_status': 'available',
                })
        return res

