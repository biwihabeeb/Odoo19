# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    revision_count = fields.Integer(
        string="Number of Revisions",
        default=0,
        compute='_compute_revision_count',
    )

    def _compute_revision_count(self):
        self.revision_count = self.env['sale.track.revision'].search_count([('order_id','=',self.id)])

    def write(self, vals):
        revision_notes = ''
        if vals and self.state == 'sent':
            for val in vals:
                if val == 'order_line':
                    revision_notes += 'Order Lines Updated\n'
                    for line in vals[val]:
                        if line[0] == 0:
                            revision_notes += 'Product: ' + line[2]['name'] + ' added to Order Lines\n'
                        elif line[0] == 1:
                            product = self.order_line.browse(line[1]).product_id
                            for key in line[2]:
                                revision_notes += f"{key} updated to {line[2][key]} for Product - {product.display_name}\n"
                        elif line[0] == 2:
                            product = self.order_line.browse(line[1]).product_id
                            revision_notes += 'Product: ' + product.display_name + ' deleted from Order Lines\n'
                else:
                    model_id = self.env['ir.model'].search([('model', '=', self._name)]).id
                    m2o_field = self.env['ir.model.fields'].search([('name', '=', val), ('model_id', '=', model_id)])
                    if m2o_field.ttype == 'many2one':
                        field_val = self.mapped(val).browse(vals[val])
                        revision_notes += val + ' updated to ' + field_val.name + '\n'
                    else:
                        revision_notes += val + ' updated to ' + str(vals[val]) + '\n'
            record = self.env['sale.track.revision'].create({
                'order_id': self.id,
                'user_id': self.env.user.id,
                'notes': revision_notes,
            })

        return super().write(vals)


    def action_view_revisions(self):
        return {
            'type': "ir.actions.act_window",
            'res_model': "sale.track.revision",
            'view_mode': 'list,form',
            'target': "current",
            'domain': [
                ('order_id','=',self.id),
            ]
        }