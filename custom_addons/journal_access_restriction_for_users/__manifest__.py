# -*- coding: utf-8 -*-


{
    'name': "Journal Access Restriction for Users",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'auto_install': True,
    'depends': [
        "base",
        "account",
    ],
    'data': [
        "views/res_users_views.xml",
    ]
}