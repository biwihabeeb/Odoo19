# -*- coding: utf-8 -*-
{
    'name': "Sale Order Revision Tracking",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'depends': [
        "base",
        "sale"
    ],
    'data': [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/sale_order_views.xml",
        "views/sale_track_revision_views.xml"
    ]
}