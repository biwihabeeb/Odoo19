# -*- coding: utf-8 -*-
from odoo import api, fields, models

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    # user_id = fields.Many2one(
    #     'res.users',
    # )

    # def _load_menus_blacklist(self):
    #     res = super()._load_menus_blacklist()
    #     hidden_menus = self.env['res.users'].search([
    #         ('id','=',self.env.user.id)
    #     ])
    #     # print(hidden_menus.mapped('hidden_menus'))
    #     # print(type(res))
    #     print('hidden menus: ',hidden_menus.mapped('hidden_menus'))
    #     if hidden_menus.mapped('hidden_menus'):
    #         for menu_item in hidden_menus.mapped('hidden_menus'):
    #             res.append(menu_item.id)
    #         print(res)
    #     return res

    # def _visible_menu_ids(self, debug=False):
    #     res = super()._visible_menu_ids(debug)
    #     hidden_menus = frozenset(self.env['res.users'].search([
    #         ('id', '=', self.env.user.id)
    #     ]).mapped('hidden_menus').ids)
    #     if hidden_menus:
    #         res = res.difference(hidden_menus)
    #     # print(res.difference(hidden_menus))
    #     print('RES:',res)
    #     print('hidden_menus:',hidden_menus)
    #     return res

    def _filter_visible_menus(self):
        res = super()._filter_visible_menus()
        hidden_menus = self.env['res.users'].search([
            ('id', '=', self.env.user.id),
        ]).mapped('hidden_menus').ids
        if hidden_menus:
            return res.filtered(lambda menu: menu.id not in hidden_menus)
        return res
