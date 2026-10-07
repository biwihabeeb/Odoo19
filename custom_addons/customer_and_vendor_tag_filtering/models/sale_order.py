# -*- coding: utf-8 -*-
from odoo import api, fields, models
from ast import literal_eval
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    allowed_tag_ids = fields.Many2many(
        'res.partner.category',
        compute='_compute_allowed_tag_ids',
        string='Allowed Customer Categories',
    )

    def _compute_allowed_tag_ids(self):
        allowed_tag_ids = self.env['ir.config_parameter'].sudo().get_param('customer_and_vendor_tag_filtering.customer_tag_ids')
        if allowed_tag_ids:
            self.allowed_tag_ids = literal_eval(allowed_tag_ids)
        else:
            self.allowed_tag_ids = False
