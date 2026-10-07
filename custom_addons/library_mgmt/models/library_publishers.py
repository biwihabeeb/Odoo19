# -*- coding: utf-8 -*-

from odoo import fields,models

class LibraryPublishers(models.Model):
    _name = 'library.publishers'
    _description = 'Publisher Records'

    name =fields.Char(
        string="Publisher Name"
    )

    publisher_address =fields.Text(
        string="Publisher Address"
    )

    books_ids = fields.One2many(
        comodel_name='library.books',
        inverse_name='book_publisher_id'
    )
