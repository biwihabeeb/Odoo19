# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class BulkPriceUpdate(models.TransientModel):
    _name = "bulk.price.update"

    price_update_method = fields.Selection(
        selection=[
            ('percent_increase', '% Increase'),
            ('percent_decrease', '% Decrease'),
            ('fixed', 'Fixed Price'),
        ],
        default='fixed',

    )

    update_value = fields.Float(
        string="Update Value",
        required=True,
    )

    # product_id = fields.Many2one(
    #     'product.product',
    # )

    product_ids = fields.One2many(
        'price.update.line',
        inverse_name="price_update_id"
    )

    def update_changes_in_price(self):
        is_group_user = self.env.user.has_group("sales_team.group_sale_manager")
        if is_group_user:
            print('Update Price')
            for line in self.product_ids:
                if line.new_price:

                    line.product_id.lst_price = line.new_price
                    # print(line.lst_price)
        else:
            raise ValidationError("User not allowed to update prices, Please Contact Sales Manager in order to make changes")

        return {
            'type': "ir.actions.act_window",
            'name': "Price Update Summary",
            'res_model': 'updated.price.summary',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_updated_product_ids': self.product_ids.ids,
                'default_update_id': self.id
            }
        }

