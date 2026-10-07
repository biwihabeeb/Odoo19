# -*- coding: utf-8 -*-
from odoo import fields, models
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_id = fields.Many2one(
         'res.partner',
     )


    vendor_tag_ids = fields.Many2many(
        'res.partner.category',
        relation="res_config_settings_vendor_tags_rel",
        string="Vendor Tags",
    )

    customer_tag_ids = fields.Many2many(
        'res.partner.category',
        string="Customer Tags",
        relation="res_config_settings_customer_tags_rel",

    )

    def set_values(self):
        res = super(ResConfigSettings,self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('customer_and_vendor_tag_filtering.customer_tag_ids',self.customer_tag_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('customer_and_vendor_tag_filtering.vendor_tag_ids',self.vendor_tag_ids.ids)
        return res
    #
    def get_values(self):
        res = super(ResConfigSettings,self).get_values()
        customer_tag_ids = self.env['ir.config_parameter'].sudo().get_param('customer_and_vendor_tag_filtering.customer_tag_ids')
        vendor_tag_ids = self.env['ir.config_parameter'].sudo().get_param('customer_and_vendor_tag_filtering.vendor_tag_ids')
        if customer_tag_ids:
            res.update({
                'customer_tag_ids': [fields.Command.set(literal_eval(customer_tag_ids))],
            })
        if vendor_tag_ids:
            res.update({
                'vendor_tag_ids': [fields.Command.set(literal_eval(vendor_tag_ids))],
            })
        return res