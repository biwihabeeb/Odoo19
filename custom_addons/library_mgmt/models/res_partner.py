# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api,fields,models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    max_borrow_count = fields.Integer(
        string="Max books borrow",
        default = lambda self: (int(self.env['ir.config_parameter'].sudo().get_param('library_mgmt.max_borrow_number'))) or 1,
        groups = "library_mgmt.group_librarian"
    )

    sum_penalty = fields.Float(
        string="Total Penalties",
        compute='_compute_sum_penalty',
        default=0.0
    )

    count_late_returns = fields.Integer(
        string="Count Late Returns",
        readonly=True
    )

    member_checkout_ids = fields.One2many(
        'library.checkouts',
        'checkout_member_name_id'
    )

    borrow_count  = fields.Integer(
        string="Number of Books Borrowed",
        compute='_compute_borrow_count'
    )

    @api.depends('member_checkout_ids.checkout_penalty')
    def _compute_sum_penalty(self):
        """
        Compute the sum of all penalties incurred for each member,
        Mapped function returns all the values in a specific field related to the
        library member in a list,
        Get the values and perform sum() to get the total incurred penalties
        """
        for rec in self:
            # print(rec.member_checkout_ids.mapped('checkout_penalty'))
            rec.sum_penalty = sum(rec.member_checkout_ids.mapped('checkout_penalty'))
            # print(self.sum_penalty)

    def _compute_borrow_count(self):
        """
        Get the number of books borrowed by each member/partner
        """
        for rec in self:
            rec.borrow_count = self.env['library.checkoutlines'].search_count([('checkout_id.checkout_member_name_id','=',rec.id),('checkout_id.checkout_status','in',['checked_out','returned','overdue'])])

    def action_view_book_checkouts(self):
        """
        View the books borrowed by each member/partner along with the checkout_id
        """
        print(self.member_checkout_ids.checkout_member_name_id.id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.checkoutlines',
            'name': 'Books Borrowed',
            'view_mode': "list",
            'domain': [('checkout_id.checkout_member_name_id','=',self.id),('checkout_id.checkout_status','in',['checked_out','returned','overdue'])]
        }

    def action_view_late_returns(self):
        """
        View checkout records with book return status marked as late
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.checkoutlines',
            'name': 'Late Returns',
            'view_mode': "list",
            'domain': [('checkout_id.checkout_member_name_id','=',self.id),('if_late','=','late')]
        }


    def penalty_amount_view(self):
        """
        View penalty amount incurred by each member
        and show checkout records with computed penalties
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.checkoutlines',
            'name': 'Penalty Amount',
            'view_mode': "list",
            'domain': [('checkout_id.checkout_member_name_id','=',self.id),('checkout_id.checkout_penalty','>',0)],
        }

