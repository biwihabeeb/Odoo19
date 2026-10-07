# -*- coding: utf-8 -*-
{
    'name': 'Merge Draft Sale Orders',
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'depends': [
        "base",
        "sale",
        "point_of_sale",
    ],
    'data': [
        "security/ir.model.access.csv",
        "data/server_action_data.xml",
        "views/sale_order_views.xml",
        "wizards/quotation_merge_views.xml",
    ]
}