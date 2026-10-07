# -*- coding: utf-8 -*-
{
    'name': 'Update Product Sales Price',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'Update Product Sales Price through Wizard',
    'installable': True,
    'auto_install': True,
    'category': 'Sales',
    'depends': [
        'base',
        'sale',
        'product',
        'sales_team',
    ],
    'data': [
        "security/ir.model.access.csv",
        "wizards/price_update_summary_view.xml",
        "wizards/sales_menu_item_bulk_price_update.xml",
    ]
}