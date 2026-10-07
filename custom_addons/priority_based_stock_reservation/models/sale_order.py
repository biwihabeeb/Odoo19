# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    priority = fields.Selection(
        [
            ('0', 'No Priority'),
            ('1', 'Low Priority'),
            ('2', 'Normal Priority'),
            ('3', 'High Priority'),
        ],
        string='Priority',
    )

    @api.model
    def action_reserve_stock_by_priority(self):
        orders = self.filtered(lambda order: order.state == 'sale')
        if not orders:
            raise ValidationError("Please select at least one confirmed order")
        # print(-int('0'))
        pickings = orders.mapped('picking_ids').sorted(key = lambda p: (-int(p.sale_id.priority or '0'), p.scheduled_date, p.id))
        for picking in pickings:
            print(picking.id)
            picking.action_assign()

        # pending = self.env['stock.picking'].search([
        #     ('state','=','confirmed'),
        #     ('sale_id','!=',False),
        #     ('picking_type_id','=',2)
        # ]).sorted(key = lambda p: (-int(p.sale_id.priority or '0'), p.scheduled_date or p.create_date, p.id))
        # print(pending,pickings)
        # for picking in pending:
        #     picking.action_assign()

