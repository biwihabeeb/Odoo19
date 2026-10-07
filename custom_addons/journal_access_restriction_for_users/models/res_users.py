# -*- coding: utf-8 -*-
from odoo import fields, models
class ResUsers(models.Model):
    _inherit = "res.users"

    allowed_journal_ids = fields.Many2many(
        'account.journal',
        groups = 'base.group_system',
    )

