# -*- coding: utf-8 -*-
{
    'name': "Associated Product",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Beevi Fathima",
    'sequence': -100,
    'application': True,
    'installable': True,
    'depends': [
        "base",
        "sale",
    ],
    'data': [
        "views/sale_order_views.xml",
        "views/res_partner_views.xml",
    ]

}