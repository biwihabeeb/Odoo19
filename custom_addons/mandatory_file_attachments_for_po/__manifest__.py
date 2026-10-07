# -*- coding: utf-8 -*-
{
    'name': "Mandatory File attachments to Confirm Purchase Orders",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'auto_install': True,
    'depends': [
        "base",
        "purchase"
    ],
    'data': [
        "views/purchase_order_views.xml",
        "views/res_conifg_settings_views_purchase.xml",
    ]
}