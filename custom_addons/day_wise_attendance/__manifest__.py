# -*- coding: utf-8 -*-
{
    'name': "Day-wise Attendance ",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'installable': True,
    'depends': [
        "base",
        "hr",
    ],
    'data': [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/hr_daily_absentees_views.xml",
    ]
}