# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.orm.decorators import readonly


class MrpProductionMaterialLine(models.Model):
    _name = 'mrp.production.material.line'

    production_id = fields.Many2one('mrp.production.ext')
    product_id = fields.Many2one('product.product')
    required_qty = fields.Float()
    available_qty = fields.Float(
        compute='_compute_available_qty',
    )
    consumed_qty = fields.Float(readonly=True)
    is_material_available = fields.Boolean(
        compute='_compute_is_material_available',
    )

    @api.depends('product_id.qty_available')
    def _compute_available_qty(self):
        for rec in self:
            if rec.product_id.qty_available != 0:
                rec.available_qty = rec.product_id.qty_available
            else:
                rec.available_qty = 0

    @api.depends('available_qty')
    def _compute_is_material_available(self):
        for rec in self:
            if rec.required_qty <= rec.available_qty:
                rec.is_material_available = True
            else:
                rec.is_material_available = False

    # @api.onchange('production_id.quantity')
    # def _onchange_quantity(self):
    #     print('QUANTITY LINE ')
