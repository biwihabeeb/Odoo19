# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    invoices_ids = fields.Many2many(
        'account.move',
    )

    currency_id = fields.Many2one(
        'res.currency',
    )

    custom_amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
    )

    def action_post(self):
        """
        - for each invoice in account_payment, create an account_payment_register wizard record
        - call action_create_payments for each record
        """
        for rec in self.invoice_ids:
            print(rec)
            environment = self.env['account.payment.register'].sudo().with_context(
                active_model='account.move', active_ids=rec.ids
            )
            print(environment)
            print(self.journal_id.name)
            recs = environment.create({
                'journal_id': self.journal_id.id,
                'payment_method_line_id': 1,
                'payment_date': date.today(),
                'amount': rec.custom_amount
            })
            print(recs)
            recs.action_create_payments()
        return super().action_post()