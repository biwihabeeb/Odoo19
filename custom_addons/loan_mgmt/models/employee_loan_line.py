# -*- coding: utf-8 -*-
from odoo import api, fields, models

class EmployeeLoanLine(models.Model):
    _name = 'employee.loan.line'
    _inherit = ['portal.mixin', 'product.catalog.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin', 'account.document.import.mixin']


    loan_id = fields.Many2one(
        'employee.loan',
    )

    amount = fields.Float(
        string='Amount',
    )

    date = fields.Date(
        string='Date',
    )

    paid = fields.Boolean(
        string='If Paid',
    )