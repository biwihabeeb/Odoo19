# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MrpProductionExt(models.Model):
    _name = 'mrp.production.ext'

    name = fields.Char(copy=False,readonly=True, default='New')

    product_id = fields.Many2one('product.product')
    bom_id = fields.Many2one('mrp.bom')
    quantity = fields.Float(required=True, string='Quantity')
    planned_date = fields.Date()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ],
        default='draft',
    )

    material_line_ids = fields.One2many(
        'mrp.production.material.line',
        inverse_name="production_id"
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Generate sequence for book records"""
        print('vals_list', vals_list)
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('mrp.production.ext') or 'New'
        return super(MrpProductionExt, self).create(vals_list)



    @api.onchange('product_id')
    def onchange_product_id(self):
        print('product_id', self.product_id)
        print('quantity', self.quantity)
        if self.product_id:
            boms = self.env['mrp.bom'].search([('product_id', '=', self.product_id.id)], limit=1)
            self.bom_id = boms.id
            print('boms', boms.bom_line_ids.mapped('product_id'))
            if self.bom_id.id:
                self.update({
                    'material_line_ids': [
                        fields.Command.clear()
                    ]
                })
                self.update({
                    'material_line_ids': [
                        fields.Command.create({
                            'product_id': bom.product_id.id,
                            'required_qty': bom.product_qty * self.quantity,
                            # 'available_qty': bom.product_id.qty_available,
                        }) for bom in boms.bom_line_ids
                    ]
                })
            else:
                raise ValidationError("No BOM found")

    @api.onchange('bom_id')
    def onchange_bom_id(self):
        print('bom_id', self.bom_id.product_id)
        if self.bom_id:
            self.update({
                'material_line_ids': [
                    fields.Command.clear()
                ]
            })
            self.update({
                'material_line_ids': [
                    fields.Command.create({
                        'product_id': line.product_id.id,
                        'required_qty': line.product_qty * self.quantity,
                        # 'available_qty': line.product_id.qty_available,
                    }) for line in self.bom_id.bom_line_ids
                ]
            })

    @api.onchange('quantity')
    def onchange_quantity(self):
        print('quantity', self.quantity)
        for line in self.material_line_ids:
            for l in self.bom_id.bom_line_ids:
                if line.product_id.id == l.product_id.id:
                    line.required_qty = l.product_qty * self.quantity

    def action_confirm_mrp(self):
        print('confirm_mrp', self.bom_id.id)
        if self.state == 'draft':
            if not self.bom_id.id:
                raise ValidationError("No BOM found")
            if self.quantity == 0:
                raise ValidationError("Quantity cannot be zero")
            self.state = 'confirmed'

    def action_mrp_set_to_draft(self):
        self.state = 'draft'

    def action_mrp_start_production(self):
        if self.state == 'confirmed':
            for line in self.material_line_ids:
                if not line.is_material_available:
                    raise ValidationError("At least one of the required Materials is unavailable")
                self.state = 'in_progress'

    def action_mrp_cancel(self):
        self.state = 'cancel'

    def action_mrp_complete_production(self):
        if self.state == 'in_progress':
            self.state = 'done'

    def action_consume_material(self):
        if self.state == 'in_progress':
            for line in self.material_line_ids:
                line.consumed_qty = line.required_qty
        pass