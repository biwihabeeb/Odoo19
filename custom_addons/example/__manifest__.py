# -*- coding: utf-8 -*-
{
    'name': "Example",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'auto_install': True,
    'depends': [
        "base",
        "product",
    ],
    'data': [
        "security/ir.model.access.csv",
        "data/example_tag_data.xml",
        "views/example_views.xml",
        "views/example_tag_views.xml",
        "views/example_line_views.xml",
        "views/example_menus.xml",
    ]
}