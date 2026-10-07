# -*- coding: utf-8 -*-
{
    'name': "Sale Order Pricelist - Auto-set",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'description': """
    Set a pricelist automatically for a customer, when a sale order is created for the customer. The price list is mapped to the country od thw customer."
    """,
    'category': 'Sales',
    'author': "Beevi Fathima",
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        "views/sale_order_views.xml",
        "security/ir.model.access.csv",
        "views/country_based_pricelist_views.xml"
    ]
}