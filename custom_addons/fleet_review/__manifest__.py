# -*- coding: utf-8 -*-
{
    'name': "Fleet",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Beevi Fathima",
    'sequence': -12,
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'fleet',
        'hr',
        'product'
    ],
    'data': [
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv",
        "views/hr_employee_views.xml",
        "views/fleet_vehicle_views.xml",
        "views/fleet_service_order_view.xml",
        "views/fleet_service_order_part_view.xml",
        "views/fleet_service_order_checklist_view.xml",
        "views/fleet_menu_view.xml",
    ]
}