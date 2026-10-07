# -*- coding: utf-8 -*-
from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    internal_remarks = fields.Text(string="Internal Remarks")