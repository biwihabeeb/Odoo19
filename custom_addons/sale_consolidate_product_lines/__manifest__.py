# -*- coding: utf-8 -*-
{
    'name': "Consolidate Duplicate Product Lines",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Beevi Fathima",
    'summary': """If there exists duplicate products in the order lines, combine the quantities of the duplicates and write as a single product line.""",
    'installable': True,
    'auto_install': False,
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        "views/sale_order_views.xml"
    ]
}