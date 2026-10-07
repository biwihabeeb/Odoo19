# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Order and Production Tracking",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'depends': [
        'base',
        'mrp'
    ],
    'data': [
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "views/mrp_production_ext_views.xml",
        "views/mrp_production_menus.xml",
    ]
}