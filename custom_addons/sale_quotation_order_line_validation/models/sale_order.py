# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_quotation_send(self):
        for record in self:
            if record.order_line.ids == []:
                raise ValidationError("You can't send a quotation order with empty order lines.")
            else:
                return super().action_quotation_send()
