# -*- coding: utf-8 -*-
from odoo import models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_suggest_alternate(self):
        unavailable_component_line_ids = self.all_move_raw_ids.filtered(lambda product: product.product_id.qty_available == 0)
        unavailable_component_ids = unavailable_component_line_ids.mapped('product_id')
        return {
            'type': "ir.actions.act_window",
            'name': "Suggested Alternate Components",
            'res_model': "mrp.suggest.alternative.component",
            'view_mode': "form",
            'target': "new",
            'context': {
                'default_unavailable_component_ids': unavailable_component_ids.ids,
                'default_order_id': self.id,
                'default_unavailable_component_line_ids': unavailable_component_line_ids.ids,
            }

        }