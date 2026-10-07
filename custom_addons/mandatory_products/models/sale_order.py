# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def unlink(self):
        lines = self.search([
            ('order_id','=',self.order_id)
        ])
        if self.product_id.associated_product_ids:
            for line in lines:
                if line.product_id in self.product_id.associated_product_ids:
                    line.unlink()
        print('lines',lines)
        return super().unlink()



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def onchange_order_line(self):
        is_mandatory = self.env['ir.config_parameter'].sudo().get_param('mandatory_products.add_mandatory_products')
        if is_mandatory:
            for line in self.order_line:
                if line.product_id.associated_product_ids:
                    self.update({
                        'order_line': [
                            fields.Command.create({
                                'product_id': product.id,
                                'product_uom_qty': 1,
                            }) for product in line.product_id.associated_product_ids
                        ]
                    })


