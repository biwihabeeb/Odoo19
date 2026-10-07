# -*- coding: utf-8 -*-
{
    'name': "Vendor Price Variance Control",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Beevi Fathima",
    'category': 'Supply Chain',
    'installable': True,
    'auto_install': True,
    'summary': """compare current purchase order unit price with the most recent PO and if the difference exceeds 15%, provide a justification""",
    'depends': [
        "base",
        "purchase",
    ],
    'data': [
        "views/purchase_order_view.xml"
    ]
}