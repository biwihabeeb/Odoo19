# -*- coding: utf-8 -*-
{
    'name': 'Loan Management',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'installable': True,
    'depends': [
        'base',
        'hr'
    ],
    'data': [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/hr_employee_views.xml",
        "views/employee_loan_line_views.xml",
        "views/employee_loan_views.xml",
        "views/employee_loan_menus.xml"
    ]
}