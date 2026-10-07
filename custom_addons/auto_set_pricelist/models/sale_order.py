# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    country_id = fields.Many2one(
        related="partner_id.country_id",
        readonly=True,
        string="Country",
    )

    @api.onchange('partner_id')
    def set_pricelist(self):
        if self.partner_id and self.partner_id.country_id:
            pricelist= self.env['country.based.pricelist'].search([
                ('country_id','=',self.partner_id.country_id.id),
            ]).mapped('pricelist_id')
            print(pricelist.id)
            if pricelist:
                self.write({
                    'pricelist_id': pricelist.id
                })
            else:
                self.write({
                    'pricelist_id': self.partner_id.property_product_pricelist.id
                })

