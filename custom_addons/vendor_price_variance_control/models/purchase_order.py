# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    justification = fields.Text(
        string="Justification",
        placeholder="Reason for alarming price variance",
    )

    flag = fields.Boolean(
        string="Flag",
    )

    def button_confirm(self):
        # print('test confirm')
        current_po = self.order_line

        last_po = self.search([
            ('id','!=', self.id),
            ('partner_id','=',self.partner_id.id),
            ('state','=','purchase'),
            ('product_id','in',current_po.mapped('product_id').ids)
        ],
            order="date_order desc",
            limit=1
        )

        # print('last PO: ',last_po)

        for current_line in current_po:
            if current_line.product_id in last_po.order_line.mapped('product_id'):
                last_line = last_po.order_line.filtered(
                    lambda line: line.product_id.id == current_line.product_id.id
                )
                current_price = current_line.price_unit
                last_price = last_line.price_unit
                variance = (last_price - current_price) / last_price
                print(self.justification)


                if variance > 0.15 and self.justification == False:
                    raise ValidationError("Price Variance exceeds the allowed 15%. Please provide justification.")

                if self.justification:
                    return super().button_confirm()
                # print('Last P0 price: ',last_line.product_id.name,last_line.price_unit)
                # print('Current PO price: ',current_line.product_id.name,current_line.price_unit)

        return super().button_confirm()

