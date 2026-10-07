# -*- coding: utf-8 -*-
from odoo import api, fields, models

class QuotationMerge(models.TransientModel):
    _name = 'quotation.merge'

    quotation_ids = fields.Many2many(
        'sale.order',
        string='Quotations',
    )

    dominated_id = fields.Many2one(
        'sale.order',
        string='Dominated Quotation',
    )

    def action_merge_quotations(self):
        order_line_ids = []
        for rec in self.quotation_ids:
            order_line_ids += rec.order_line
        for line in order_line_ids:
            print('all order lines: ', line)
            if line.product_id in self.dominated_id.order_line.mapped('product_id'):
                order_line = self.dominated_id.order_line.filtered(lambda l: l.product_id.id == line.product_id.id)
                order_line.product_uom_qty += line.product_uom_qty
            else:
                self.dominated_id.write({
                    'order_line': [
                        fields.Command.create({
                            'product_id': line.product_id.id,
                            'product_uom_qty': line.product_uom_qty,
                        })
                    ]
                })
        for rec in self.quotation_ids:
            if self.dominated_id.id != rec.id:
                rec.state = 'cancel'