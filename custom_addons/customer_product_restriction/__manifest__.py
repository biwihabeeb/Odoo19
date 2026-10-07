# -*- coding: utf-8 -*-
{
    'name': "Customer Product Restriction",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'depends': [
        "base",
        "product",
        "sale",
    ],
    'data': [
        "views/res_partner_views.xml",
        "views/sale_order_line_views.xml",
    ]
}