# -*- coding: utf-8 -*-
{
    'name': "Employee Contract Expiry Email",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'depends': [
        "base",
        "hr"
    ],
    'data': [
        "data/email_template.xml",
        "data/scheduled_action.xml",
        "views/res_config_settings_views.xml",
    ],
    'installable': True,
}