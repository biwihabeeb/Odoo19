# -*- coding: utf-8 -*-
from odoo import fields, models

class MrpSuggestAlternativeComponent(models.TransientModel):
    _name = 'mrp.suggest.alternative.component'

    order_id = fields.Many2one(
        'mrp.production'
    )

    unavailable_component_ids = fields.Many2many(
        'product.product',
        string='Unavailable Components',
    )

    unavailable_component_line_ids = fields.Many2many(
        'stock.move'
    )

    def add_component(self):

        for line in self.unavailable_component_line_ids:
            if line.product_id.alternate_component_id:
                self.order_id.update({
                    'all_move_raw_ids': [
                        fields.Command.unlink(line.id)
                    ],
                })

        for component in self.unavailable_component_ids:
            if component.alternate_component_id:
                self.order_id.update({
                    'all_move_raw_ids': [
                        fields.Command.create({
                            'product_id': component.alternate_component_id.id,
                            'product_uom_qty': 1,
                        })
                    ]
                })

