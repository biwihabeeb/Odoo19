# -*- coding: utf-8 -*-
{
    'name': 'Delivery Slip Internal Remarks',
    'version': '19.0.1.0.0',
    'license': "LGPL-3",
    'installable': True,
    'auto_install': False,
    'depends': [
        'base',
        'stock'
    ],
    'data': [
        "reports/stock_picking_text_field_report_view.xml",
        "views/stock_picking_new_field_view.xml",
    ]
}