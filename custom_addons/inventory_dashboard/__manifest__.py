# -*- coding: utf-8 -*-
{
    'name': "Inventory Dashboard",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'depends': [
        "base",
        "stock"
    ],
    'data': [
        "data/client_actions.xml"
    ],
    'assets': {
        'web.assets_backend': [
            "inventory_dashboard/static/src/js/dashboard.js",
            "inventory_dashboard/static/src/xml/inventory_dashboard_template.xml",
        ]
    }
}