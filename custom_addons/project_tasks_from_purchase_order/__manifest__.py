# -*- coding: utf-8 -*-
{
    'name': "Project Tasks from Purchase Orders",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'summary': """Generate Tasks in Projects that are linked to products in a Purchase Order""",
    'installable': True,
    'auto_install': True,
    'depends': [
        "base",
        "purchase",
        "product",
        "project",
    ],
    'data': [
        "views/product_product_views.xml",
    ]
}