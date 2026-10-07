# -*- coding: utf-8 -*-
from email.policy import default

from PIL.ImageChops import offset
from twilio.rest.api.v2010.account.usage.record import today
from twilio.rest.memory.v1 import store

from odoo.tools import date_utils

from odoo import api,fields,models
from datetime import date,timedelta
from odoo.exceptions import ValidationError
from odoo.orm.decorators import readonly


class LibraryCheckouts(models.Model):
    _name = 'library.checkouts'
    _description = 'Checkout Records'

    name = fields.Char(
        string="Checkout ID",
        required=True,
        readonly=True,
        default=lambda self:'New'
    )

    checkout_member_name_id = fields.Many2one(
        comodel_name='res.partner',
        string="Member Name",
        required=True,
    )

    checkout_member_contact = fields.Char(
        related="checkout_member_name_id.phone",
        string="Member Contact"
    )

    checkout_member_email = fields.Char(
        related="checkout_member_name_id.email",
        string="Member Email",
        store=True
    )

    checkout_lines_ids = fields.One2many(
        "library.checkoutlines",
        "checkout_id"
    )

    checkout_date = fields.Date(
        string="Date of Checkout"
    )

    checkout_return_due = fields.Date(
        string="Expected Return date"
    )

    checkout_returned = fields.Date(
        string="Returned Date"
    )

    checkout_penalty = fields.Float(
        string="Fine to pay (if any)",
        compute='_compute_checkout_penalty',
        store=True,
        readonly=True
    )

    checkout_status = fields.Selection(
        [('checked_out','Checked Out'),('returned','Returned'),('overdue','Overdue')],
        string="Status"
    )

    if_late_return = fields.Selection(
        [('on_time','On Time Return'),('late','Late Return'),('not','Not Returned')],
        string="Return status",

    )

    invoice_id = fields.Many2one(
        comodel_name='account.move',
        readonly=True
    )

    invoice_count = fields.Integer(
        string="Invoice Count",
        compute='_compute_invoice_count',
    )

    payment_status = fields.Selection(
        [('paid','Paid'),('not_paid','Not Paid')],
        compute='_get_payment_status',
        default=False,
        readonly=True,
    )

    late_return_limit_warning_text = fields.Text(
        default= False,
        compute='_compute_late_return_limit_warning_text'
    )

    def _get_payment_status(self):
        """
        Set the checkout's payment status depending on the related invoice's status_in_payment
        """
        if self.env['account.move'].search([('checkout_id','=',self.id),('checkout_id.checkout_member_name_id','=',self.checkout_member_name_id.id),('status_in_payment','=','paid')]):
            self.payment_status = 'paid'
        else:
            self.payment_status = 'not_paid'


    def _compute_invoice_count(self):
        """
        Compute the number of invoices created for a checkout record
        """
        self.invoice_count = self.env['account.move'].search_count([('checkout_id','=',self.id)])
        print(self.invoice_count)

    def action_view_invoices(self):
        """
        View invoices related to a ceckout record
        """
        return {
            'type': "ir.actions.act_window",
            'res_model': "account.move",
            'name': "Invoice",
            'view_mode': "list,form",
            'domain': [('checkout_id','=',self.id),('checkout_id.checkout_member_name_id','=',self.checkout_member_name_id.id)]
        }

    @api.model
    def _compute_late_return_limit_warning_text(self):
        """
        Get a warning message when checkout records are being created for members who repeatedly
        failed to return borrowed books on time
        """
        max_limit = int(self.env['ir.config_parameter'].sudo().get_param('library_mgmt.max_allowed_late_returns'))
        recs= self.search([('checkout_member_name_id','=',self.checkout_member_name_id.id)])
        for rec in recs:
            member = rec.checkout_member_name_id
            if member.count_late_returns == (max_limit)//2 and member.count_late_returns <= max_limit and member.count_late_returns !=0:
                rec.write({
                    'late_return_limit_warning_text': "This member has repeatedly failed to return checked out books within the expected duration",
                })
            else:
                rec.write({
                    'late_return_limit_warning_text': False
                })


    @api.depends('checkout_return_due','checkout_returned','checkout_date')
    def _compute_checkout_penalty(self):
        """
        compute the penalty for late returns or overdue checkouts and store in
        th checkout_penalty field
        """
        penalty = float(self.env['ir.config_parameter'].sudo().get_param('library_mgmt.penalty_per_hour'))
        for rec in self:
            late_days = 0
            if rec.checkout_return_due and rec.checkout_date:
                if rec.checkout_returned:
                    if (rec.checkout_returned-rec.checkout_return_due).days > 0:
                         late_days = (rec.checkout_returned-rec.checkout_return_due).days
                else:
                    today = date.today()
                    if (today-rec.checkout_return_due).days > 0:
                        late_days = (today-rec.checkout_return_due).days
                rec.checkout_penalty = late_days * penalty * 24.0
            else:
                rec.checkout_penalty = 0.0
            rec.checkout_member_name_id.sum_penalty += rec.checkout_penalty
            # print(rec.checkout_penalty)

    @api.constrains('checkout_lines_ids','checkout_member_name_id')
    def _check_max_borrow(self):
        """
        Check if the member's book borrow count exceeds the default system parameter value
        """
        for checkout in self:
            if not checkout.checkout_member_name_id:
                continue
            max_books = checkout.checkout_member_name_id.max_borrow_count or 1
            if len(checkout.checkout_lines_ids)>max_books:
                raise ValidationError(f"This member has reached maximum limit {max_books} for books to borrow")

    @api.model_create_multi
    def create(self, vals_list):
        """
        Generate sequence for checkout records
        """
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('library.checkouts') or 'New'
        return super(LibraryCheckouts, self).create(vals_list)

    def button_checkout(self):
        """Checkout button action
        ------------------------------
        sets the checkout date,
        calculates expected return date,
        sets the checkout status to {checked_out},
        sets the book status to {unavailable},
        open a wizard suggesting similar books
        """
        return_pending = self.search([('checkout_status', '=', 'checked_out'),('if_late_return','=','not'),('checkout_member_name_id','=',self.checkout_member_name_id.id)])
        if return_pending:
            raise ValidationError("This member has pending books to return")
        for rec in self:
            # print(rec.checkout_lines_ids.book_id.book_title)
            # if rec.checkout_lines_ids.book_id.book_title == False:
            #     raise ValidationError("No books added to proceed")

            rec.if_late_return = 'not'
            rec.checkout_lines_ids.book_id.book_status = 'unavailable'
            rec.checkout_status = 'checked_out'
            rec.checkout_date = date.today()
            add_days = rec.env['ir.config_parameter'].sudo().get_param('library_mgmt.max_borrow_days')
            # print(int(add_days))
            rec.checkout_return_due = rec.checkout_date + timedelta(int(add_days))
            max_late_return_limit = int(self.env['ir.config_parameter'].sudo().get_param('library_mgmt.max_allowed_late_returns'))
            print(max_late_return_limit)
            member = self.checkout_member_name_id
            overdue = self.search([('checkout_member_name_id','=',member.id),('checkout_status','=','overdue')])
            if member.count_late_returns >= max_late_return_limit:
                raise ValidationError("This member has exceeded the permissible number of late book returns. Hence, new book checkouts will be blocked")
            if overdue:
                raise ValidationError("This member has overdue books yet to be returned")

        same_author_ids = self.env['library.books'].search([
            ('book_author_id','=',self.checkout_lines_ids.book_id.book_author_id),
            ('book_status','=','available')
        ]).ids

        same_genre_ids = self.env['library.books'].search([
            ('book_genre_ids','=',self.checkout_lines_ids.book_id.book_genre_ids),
            ('book_status','=','available')
        ]).ids

        popular_books = self.env['library.books'].search(
            [('book_status','=','available'),('book_borrow_count','!=',0)],
            order='book_borrow_count desc',
            limit=2).ids

        book_suggestions_ids = same_author_ids + same_genre_ids + popular_books

        return {
            'type': 'ir.actions.act_window',
            'name': 'More Suggestions',
            'res_model': 'library.book.suggestions',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_suggestion_ids': book_suggestions_ids,
                        'default_checkout_id': self.id,
                        },
        }

    def button_return(self):
        """Return button actions
        --------------------------
        sets the returned date,
        sets the book status back to {available},
        sets the checkout status to {returned},
        open a wizard suggesting similar books,
        check condition if the book is returned after the due date and set the return_status
        """
        for rec in self:
            if rec.checkout_status != 'checked_out':
                raise ValidationError("Books not checked out to return")
            for book in self.checkout_lines_ids:
                book.book_id.book_borrow_count += 1

            rec.checkout_status = 'returned'
            rec.checkout_returned = date.today()
            member= rec.checkout_member_name_id
            if rec.checkout_return_due < rec.checkout_returned:
                rec.if_late_return = 'late'
                member.count_late_returns += 1
            else:
                rec.if_late_return = 'on_time'
            print(member.count_late_returns)

    def create_invoice(self):
        """
        Create invoice for related checkout
        """
        invoice = self.env['account.move'].create({
            'move_type': "out_invoice",
            'partner_id': self.checkout_member_name_id.id,
            'checkout_id': self.id,
            'invoice_line_ids': [
                fields.Command.create({
                    'name': rec.book_id.book_title,
                    'price_unit': rec.book_id.book_price,
                }) for rec in self.checkout_lines_ids
            ]
        })
        if self.checkout_penalty:
            invoice.update({
                'invoice_line_ids': [
                    fields.Command.create({
                        'name': "Late Return Penalty",
                        'price_unit': self.checkout_penalty
                    })
                ]
            })

        return {
            'type': "ir.actions.act_window",
            'res_model': "account.move",
            'name': "Draft Invoice",
            'view_mode': "form",
            'target': "current",
            'res_id': invoice.id,

        }

    def button_cancel(self):
        """Cancel button action
        -------------------------
        resets the date fields and status to null
        """
        for rec in self:
            rec.if_late_return = None
            rec.checkout_lines_ids.book_id.book_status = 'available'
            rec.checkout_status = None
            rec.checkout_returned = None
            rec.checkout_date = None
            rec.checkout_return_due = None

    @api.model
    def send_reminder(self):
        """
        Send reminder mail to member n days before the book's expected return date
        """
        reminder_days = self.env['ir.config_parameter'].sudo().get_param('library_mgmt.reminder_days')
        max_borrow = self.env['ir.config_parameter'].sudo().get_param('library_mgmt.max_borrow_days')
        offset_days = int(max_borrow)-int(reminder_days)
        checkouts = self.search([('checkout_status','=','checked_out')])
        today = date.today()
        template = self.env.ref("library_mgmt.email_template_book_return_reminder")
        for rec in checkouts:
            if (rec.checkout_date)+timedelta(offset_days)==today:
                template.send_mail(rec.id, force_send=True)

    @api.model
    def send_overdue_notice(self):
        """
        Send email to a member when a checkout is overdue
        """
        today = date.today()
        print( self.search([]).mapped('checkout_return_due'))
        overdue = self.search([('checkout_status','=','checked_out'),('checkout_return_due','<',today)])
        template = self.env.ref("library_mgmt.email_template_book_return_overdue")
        for checkout in overdue:
            checkout.checkout_status = 'overdue'
            test = template.send_mail(checkout.id,force_send=True)







