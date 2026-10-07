# -*- coding: utf-8 -*-
from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    partner_allowed_product_ids = fields.Many2many(
        related='order_partner_id.allowed_product_ids'
    )