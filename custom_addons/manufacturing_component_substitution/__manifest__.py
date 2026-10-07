# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Component Substitution",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'depends': [
        "base",
        "product",
        "mrp",
        "stock",
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/mrp_production_views.xml",
        "views/product_product_views.xml",
        "wizards/mrp_suggest_alternative_component_views.xml",
    ]
}