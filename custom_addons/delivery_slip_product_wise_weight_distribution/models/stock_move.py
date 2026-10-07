# -*- coding: utf-8 -*-
from odoo import api, fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    line_weight = fields.Float(
        string="Total Product Weight (in kg)",
        compute="_compute_line_weight",
    )

    @api.depends('quantity', 'product_id.weight')
    def _compute_line_weight(self):
        for move in self:
            if move.quantity and move.product_id.weight:
                move.line_weight = move.quantity * move.product_id.weight
            else:
                move.line_weight = 0.0