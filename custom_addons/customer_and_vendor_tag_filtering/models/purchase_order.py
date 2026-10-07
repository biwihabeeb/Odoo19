# -*- coding: utf-8 -*-

from odoo import api, fields, models
from ast import literal_eval

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    allowed_tag_ids = fields.Many2many(
        'res.partner.category',
        compute='_compute_allowed_tag_ids',
        string='Allowed Vendor Categories',
    )

    def _compute_allowed_tag_ids(self):
        allowed_tag_ids = self.env['ir.config_parameter'].sudo().get_param('customer_and_vendor_tag_filtering.vendor_tag_ids')
        if allowed_tag_ids:
            self.allowed_tag_ids = literal_eval(allowed_tag_ids)
        else:
            self.allowed_tag_ids = False