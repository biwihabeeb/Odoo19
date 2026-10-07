# -*- coding: utf-8 -*-
from openpyxl.worksheet import related

from odoo import  api,fields, models
class LibraryCheckoutLines(models.Model):
    _name = 'library.checkoutlines'
    _description = 'Checkout Lines'
    _rec_name = 'book_title'

    checkout_id = fields.Many2one("library.checkouts")
    book_id = fields.Many2one(
        "library.books",
        domain=[('book_status','=','available')]
    )

    checkout_name = fields.Char(
        related='checkout_id.name',
        string="Checkout ID",
    )

    checkout_date = fields.Date(
        related='checkout_id.checkout_date',
        string="Checkout Date",
    )

    return_date = fields.Date(
        related='checkout_id.checkout_returned',
        string = "Return Date",
    )

    checkout_status = fields.Selection(
        related='checkout_id.checkout_status',
        string="Checkout Status",
    )

    if_late = fields.Selection(
        related='checkout_id.if_late_return',
    )

    checkout_penalty = fields.Float(
        related='checkout_id.checkout_penalty',
    )

    book_title = fields.Char(
        related="book_id.book_title"
    )

    book_status = fields.Selection(
        related="book_id.book_status"
    )

    book_author_id = fields.Many2one(
        related="book_id.book_author_id"
    )

    book_genre_ids = fields.Many2many(
        related="book_id.book_genre_ids"
    )

    _book_added = models.Constraint(
        'UNIQUE(checkout_id, book_id)',
        'Book has already been added'
    )


