# -*- coding: utf-8 -*-
{
    'name': 'Equipment Reservation',
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'summary': """Equipment Reservation""",
    'depends': [
        "base",
        "hr",
        "product"
    ],
    'data': [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/ir_sequence_data.xml",
        "views/reserve_equipment_line_views.xml",
        "views/reserve_equipment_views.xml",
        "views/reserve_equipment_menus.xml"
    ]
}