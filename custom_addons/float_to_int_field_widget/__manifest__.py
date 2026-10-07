# -*- coding: utf-8 -*-
{
    'name': "Float to Integer Field Widget",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'depends': [
        "base",
        "sale"
    ],
    'data': [
        # "views/sale_order_views.xml",
        "views/sale_order_views.xml"
    ],
    'assets': {
        'web.assets_backend': [
            "float_to_int_field_widget/static/src/js/field_widget.js",
            "float_to_int_field_widget/static/src/xml/field_widget.xml"
        ]
    }
}