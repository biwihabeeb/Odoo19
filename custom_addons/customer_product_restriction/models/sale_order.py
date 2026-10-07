# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_allowed_product_ids = fields.Many2many(
        related='partner_id.allowed_product_ids'
    )

    def action_confirm(self):
        group_user = self.env.user.has_group('sales_team.group_sale_manager')
        print(len(self.order_line), self.partner_id.order_limit)
        if not group_user:
            if len(self.order_line) > self.partner_id.order_limit:
                raise ValidationError(f"This order exceeds the order limit of products for the partner. Order Limit: {self.partner_id.order_limit}")
        return super().action_confirm()
