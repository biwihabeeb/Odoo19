# -*- coding: utf-8 -*-
from odoo import models
from odoo.fields import Domain


class IrRule(models.Model):
    _inherit = "ir.rule"

    def _compute_domain(self,model_name,mode='read'):
        res = super()._compute_domain(model_name,mode)
        if model_name=='account.move':
            return Domain.AND([
                res,
                [('journal_id', 'in', self.env.user.allowed_journal_ids.ids)]
            ])
        if model_name=='account.move.line':
            return Domain.AND([
                res,
                [('journal_id', 'in', self.env.user.allowed_journal_ids.ids)]
            ])
        if model_name=='account.journal':
            # print('Search: ', self.env[model_name].sudo().search([]).mapped('name'))
            if self.env.user.allowed_journal_ids.ids == []:
                journal_ids = self.env[model_name].sudo().search([]).ids
            else:
                journal_ids = self.env.user.allowed_journal_ids.ids
            return Domain.AND([
                res,
                [('id','in',journal_ids)]
            ])

        else:
            return res