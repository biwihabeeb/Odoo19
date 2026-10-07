# -*- coding: utf-8 -*-
{
    'name': "Mandatory Product",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'summary': """Add Mandatory Products associated witha product to SO""",
    'depends': [
        "base",
        "product",
        "sale",
    ],
    'data': [
        "views/product_product_views.xml",
        "views/res_config_settings_views.xml",
    ]
}