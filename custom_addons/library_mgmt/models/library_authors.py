# -*- coding: utf-8 -*-

from odoo import fields, models

class LibraryAuthors(models.Model):
    _name = 'library.authors'
    _description = 'Author Records'


    name = fields.Char(
        string="Author Name",
        required=True)

    author_books_ids = fields.One2many(
        comodel_name='library.books',
        string="Books",
        inverse_name='book_author_id')