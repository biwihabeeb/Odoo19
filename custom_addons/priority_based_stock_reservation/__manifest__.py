# -*- coding: utf-8 -*-
{
    'name': "Priority Based Stock Reservation",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'depends': [
        "stock",
        "sale",
        "base"
    ],
    'installable': True,
    'data': [
        "data/ir_actions_server.xml",
        # "views/res_partner_views.xml",
        "views/sale_order_views.xml",
    ],
}