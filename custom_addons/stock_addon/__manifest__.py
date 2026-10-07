# -*- coding: utf-8 -*-
{
    'name': "Stock Addon",
    'version': "19.0.1.0",
    'license': "LGPL-3",
    'author': "Cybrosys Tech Solutuions",
    'website': "http://www.cybrosys.com",
    'category': "Quick",
    'summary': """"Quick Tasks""",
    'sequence': -11,
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': [
        "base",
        "stock",
    ],
    'data': [
        "data/data_stock_location.xml",
    ],

}