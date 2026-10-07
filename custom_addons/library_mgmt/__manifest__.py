# -*- coding: utf-8 -*-
{
    'name':"Library Management",
    'version': "19.0.1.0",
    'license': "LGPL-3",
    'author': "Cybrosys Tech Solutions",
    'website': "http://www.cybrosys.com",
    'category': 'Eductation',
    'summary':"""An ERP for Library Management""",
    'description':"""Manage your Library with Odoo""",
    'sequence':-10,
    'application':True,
    'installable':True,
    'auto_install':True,
    'depends': [
        "web",
        "base",
        "mail",
        "account",
        "product",

    ],
    'data':[
        "security/library_mgmt_groups.xml",
        "security/record_rules.xml",
        "security/ir.model.access.csv",
        "wizards/library_book_borrow_report_views.xml",
        "reports/library_book_borrow_report_template.xml",
        "reports/library_book_borrow_report.xml",
        "data/ir_mail_server.xml",
        "data/ir_cron.xml",
        "data/email_template.xml",
        "data/demo_genre_data.xml",
        "data/ir_sequence_data.xml",
        "views/snippets/trending_books_content.xml",
        "views/snippets/trending_books_carousel_snippet.xml",
        "views/library_portal_book_donation_view_template.xml",
        "views/book_donation_form.xml",
        "views/library_config_settings_views.xml",
        "views/library_checkoutlines_view.xml",
        "views/library_members_view.xml",
        "views/library_publishers_views.xml",
        "views/library_genres_views.xml",
        "views/library_checkouts_views.xml",
        "views/library_authors_views.xml",
        "views/library_books_views.xml",
        "views/library_mgmt_menus.xml",
        "wizards/library_suggestion_views.xml",

    ],
    'assets':{
        'web.assets_backend': [
            "library_mgmt/static/src/js/action_manager.js",
            # "library_mgmt/static/src/js/multi_select_genres.js"
        ],
        'web.assets_frontend': [
            "library_mgmt/static/src/js/trending_books_snippet.js",
            "library_mgmt/static/src/xml/trending_books_snippet_template.xml",
            "library_mgmt/static/src/img/noun-book-1069597.svg",
        ]
    },
}