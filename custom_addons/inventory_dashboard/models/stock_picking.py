# -*- coding: utf-8 -*-
from odoo import api, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # @api.model
    # def get_internal_transfers(self):
    #     pass