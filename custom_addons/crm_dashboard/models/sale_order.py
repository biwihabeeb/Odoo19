# -*- coding: utf-8 -*-
from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        if self.opportunity_id.stage_id.name != self.opportunity_id.team_id.stage_id.name:
            self.opportunity_id.stage_id = self.opportunity_id.team_id.stage_id.id
        return super().action_confirm()