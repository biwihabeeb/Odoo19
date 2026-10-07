# -*- coding: utf-8 -*-
{
    'name': "CRM Dashboard",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'depends': [
        "base",
        "crm",
        "sales_team",
        "sale",
    ],
    'data': [
        "data/client_actions.xml",
        "views/crm_team_views.xml"
    ],
    'assets': {
        'web.assets_backend': [
            "crm_dashboard/static/src/js/dashboard.js",
            "crm_dashboard/static/src/xml/crm_dashboard_template.xml",
        ]
    }
}