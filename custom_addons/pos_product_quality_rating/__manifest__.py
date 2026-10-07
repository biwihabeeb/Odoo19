# -*- coding: utf-8 -*-
{
    'name': "POS Product Quality Rating",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'depends': [
        "base",
        "point_of_sale",
        "product",
    ],
    'data': [
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            "pos_product_quality_rating/static/src/xml/quality_rating.xml",
        ]
    }
}