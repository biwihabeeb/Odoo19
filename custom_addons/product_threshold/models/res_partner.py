# -*- coding: utf-8 -*-
from odoo import api, fields, models



class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_ids = fields.Many2many(
        'product.product',
        string='Products',
    )

    def action_recalculate(self):
        threshold = self.env['ir.config_parameter'].sudo().get_param('product_threshold.product_threshold')
        products = self.env['sale.order.line'].search([
            ('order_partner_id','=', self.id),
            ('product_uom_qty','>=',threshold),
        ]).mapped('product_id')

        self.product_ids = products
        print('Field update',self.product_ids)

    def action_add_to_so(self):
        threshold = self.env['ir.config_parameter'].sudo().get_param('product_threshold.product_threshold')
        print('products in self: ',self.product_ids)

        if self.product_ids:
            sale_order = self.env['sale.order'].create({
                'partner_id': self.id,
                'order_line': [fields.Command.create({
                    'product_id': product.id,
                    'product_uom_qty': threshold,
                }) for product in self.product_ids
                ]
            })
            print(sale_order)
        return {
            'type': "ir.actions.client",
            'tag': "display_notification",
            'params': {
                'title': "Sale Order Quotation Created",
                'message': f"{sale_order.mapped('name')}",
                'type': "success",
                'sticky': False,
            }
        }
