# -*- coding: utf-8 -*-
from odoo import fields, models
import math


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def round_off_invoice_amount(self):
        invoices = self.env['account.move'].search([
            ('partner_id', '=', self.id),
            ('status_in_payment', '=', 'draft')
        ])
        # print(invoices)
        for invoice in invoices:
            original = invoice.amount_total_in_currency_signed
            rounded = math.floor(original)
            round_off = round(rounded - original,2)
            if round_off != 0.0:
                invoice.update({
                    'invoice_line_ids': [
                        fields.Command.create({
                            'name': "Round Off",
                            'quantity': 1,
                            'price_unit': round_off,
                        })
                    ],
                    'amount_residual': rounded,
                })

