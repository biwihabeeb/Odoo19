# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EmployeeLoan(models.Model):
    _name = 'employee.loan'
    _inherit = ['portal.mixin', 'product.catalog.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin', 'account.document.import.mixin']

    name = fields.Char(
        required=True,
        default='New',
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
        domain=[
            ('loan_not_allowed', '!=', True),
        ]
    )

    loan_amount = fields.Float(
        string='Loan Amount',
    )
    installment_count = fields.Integer(
        string='Installment Count',
    )
    start_date = fields.Date(
        string='Start Date',
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('approved', 'Approved'),
         ('ongoing', 'Ongoing'),
         ('paid', 'Paid'),
        ],
        string='Status',
        default='draft',
    )

    loan_line_ids = fields.One2many(
        'employee.loan.line',
        inverse_name='loan_id',
    )

    total_payable = fields.Float(
        string='Total Payable',
        compute='_compute_total_payable',
    )

    installment_amount = fields.Float(
        string='Installment Amount',
    )

    loan_lines_count = fields.Integer(
        string='Loan Lines Count',
        compute='_compute_loan_lines_count',
    )

    paid_amount = fields.Float(
        string='Paid Amount',
        compute='_compute_paid_amount',
    )

    balance_amount = fields.Float(
        string='Balance Amount',
        compute='_compute_balance_amount',
    )

    @api.depends('loan_line_ids')
    def _compute_paid_amount(self):
        for rec in self:
            paid_installments = rec.loan_line_ids.filtered(lambda line: line.paid == True)
            rec.paid_amount = sum(paid_installments.mapped('amount'))

    @api.depends('loan_amount','paid_amount')
    def _compute_balance_amount(self):
        for rec in self:
            rec.balance_amount = rec.loan_amount - rec.paid_amount

    @api.depends('loan_line_ids')
    def _compute_loan_lines_count(self):
        for rec in self:
            rec.loan_lines_count = len(rec.loan_line_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name','New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('employee.loan') or 'New'
        return super(EmployeeLoan, self).create(vals_list)

    @api.onchange('loan_amount','installment_count')
    def _onchange_loan_amount(self):
        if self.loan_amount and self.installment_count:
            self.installment_amount = self.loan_amount / self.installment_count
        else:
            self.installment_amount = self.loan_amount or 0.0


    @api.depends('loan_line_ids')
    def _compute_total_payable(self):
        for rec in self:
            if rec.loan_line_ids:
                rec.total_payable = sum(rec.loan_line_ids.mapped('amount'))
            else:
                rec.total_payable = 0.0

    def action_approve(self):
        if self.state == 'draft':
            if self.loan_amount > 0:
                self.state = 'approved'
            else:
                raise ValidationError("Loan amount is negative or zero")

    def action_view_loan_lines(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'employee.loan.line',
            'name': 'Loan Lines',
            'view_mode': 'list',
            'domain': [
                ('loan_id','=',self.id),
            ]
        }

    def generate_installments(self):
        if self.state == 'approved':
            self.update({
                'loan_line_ids': [
                    fields.Command.create({
                        'loan_id': self.id,
                        'amount': self.installment_amount,
                    }) for i in range(self.installment_count)
                ]
            })
            self.state = 'ongoing'

    def action_loan_payment(self):
        if self.state == 'ongoing':
            installments = self.loan_line_ids.filtered(lambda line: line.paid != True)
            if len(installments) == 1:
                self.state = 'paid'
            installments[0].paid = True








