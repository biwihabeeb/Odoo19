# -*- coding: utf-8 -*-
{
    'name': "Combined Invoice Payment",
    'version': "19.0.1.0.0",
    'category': "Finance",
    'license': "LGPL-3",
    'author': "Beevi Fathima",
    'installable': True,
    'auto_install': False,
    'summary': """display partner specific invoices in the payment form view,
    allow selection of invoices and add field to input custom amount for each selected invoice, and initiate payment.""",
    'depends': [
        "base",
        "account"
    ],
    'data': [
        "views/account_payment_views.xml"
    ]
}