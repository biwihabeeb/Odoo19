# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_prime_Customer = fields.Boolean(
        string="Prime Customer",
    )