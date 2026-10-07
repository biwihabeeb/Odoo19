# -*- coding: utf-8 -*-
{
    'name': 'Product-wise Weight Split in Delivery Slip',
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Beevi Fathima",
    'installable': True,
    'depends': [
        "base",
        "stock",
    ],
    'data': [
        "reports/delivery_slip_line_weight.xml",
        "views/stock_picking_views.xml",
    ]
}