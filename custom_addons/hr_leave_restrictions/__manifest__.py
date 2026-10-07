# -*- coding: utf-8 -*-
{
    'name': "HR Leave Restrictions",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Beevi Fathima",
    'category': "Human Resources",
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'hr',
    ],
    'data': [
        "views/hr_leave_views.xml",
    ]
}