# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleTrackRevision(models.Model):
    _name = 'sale.track.revision'

    name = fields.Char(
        string="Revision Number",
        required=True,
        default="New"
    )

    notes = fields.Text(
        string="Revision Notes",
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
    )

    order_id = fields.Many2one(
        'sale.order'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.track.revision') or 'New'
        return super(SaleTrackRevision, self).create(vals_list)



