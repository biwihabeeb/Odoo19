# -*- coding: utf-8 -*-
{
    'name': "Customer & Vendor Tag Filtering",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Beevi Fathima",
    'summary': """Configure Customer and Vendor Tag Filtering in Orders""",
    'installable': True,
    'auto_install': True,
    'depends': [
        "base",
        "sale",
        "purchase",
    ],
    'data': [
        "views/sale_order_views.xml",
        "views/purchase_order_views.xml",
        "views/res_config_settings_views.xml"
    ]

}