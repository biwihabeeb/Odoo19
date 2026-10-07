# -*- coding: utf-8 -*-
{
    'name': "POS Purchase Limit",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'author': "Beevi Fathima",
    'depends': [
        "base",
        "point_of_sale",
    ],
    'data': [
        "views/res_partner_views.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            "pos_purchase_limit/static/src/js/purchase_limit_validation.js"
        ]
    }
}