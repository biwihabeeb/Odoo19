# -*- coding: utf-8 -*-
from odoo import api, fields, models

class CountryBasedPricelist(models.Model):
    _name = 'country.based.pricelist'

    country_id = fields.Many2one(
        'res.country'
    )

    pricelist_id = fields.Many2one(
        'product.pricelist'
    )