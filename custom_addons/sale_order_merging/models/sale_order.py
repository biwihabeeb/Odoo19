# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    session_id = fields.Many2one(
        'pos.session',
    )

    def action_merge_draft_so(self):
        action = {
            'type': "ir.actions.act_window",
            'name': "Merge Quotations",
            'res_model': 'quotation.merge',
            'view_mode': "form",
            'target': 'new',
            'context': {
                'default_quotation_ids': self.ids,
            }
        }
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError("Only quotations in draft stage can be merged")
        if len(self.mapped('partner_id')) > 1:
            raise ValidationError("Only quotations belonging to the same partner are allowed to merge")
        return action

    def action_pay_at_counter(self):
        pass




