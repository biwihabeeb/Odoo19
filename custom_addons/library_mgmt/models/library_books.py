# -*- coding: utf-8 -*-
from os import read

from openpyxl.worksheet import related

from odoo import api,fields,models
from odoo.exceptions import ValidationError

class LibraryBooks(models.Model):
    _name = 'library.books'
    _description = 'Library Book Records'
    _rec_name = 'book_title'

    name = fields.Char(
        string="Book ID",
        readonly=True,
        default=lambda self: 'New',copy=False)

    book_title = fields.Char(
        string="Title",
        required=True)

    book_cover = fields.Image(
        max_height=100,
        max_width=60)

    book_isbn = fields.Char(
        string="ISBN",
        copy=False,
        required=True,
    )

    _isbn_uniqueness = models.Constraint(
        'UNIQUE(book_isbn)',
        'ISBN Code should be unique'
    )

    book_status = fields.Selection(
        [('available','Available'),('unavailable','Unavailable'),('coming_soon','Coming Soon')],
        string="Status",
        default='available')

    book_author_id = fields.Many2one(
        comodel_name='library.authors',
        string="Author")

    book_publisher_id = fields.Many2one(
        comodel_name='library.publishers',
        string="Publisher")

    book_genre_ids = fields.Many2many(
        comodel_name='library.genres',
        string="Genre")

    book_language_id = fields.Many2one(
        'res.lang',
        string="Language",
    )

    currency_id = fields.Many2one('res.currency')

    book_price = fields.Monetary(
        string="Price",
        currency_field="currency_id")

    book_cost = fields.Monetary(
        string="Management Cost",
        currency_field="currency_id")

    book_borrow_count = fields.Integer(
        string="Book Borrow Count",
        readonly=True
    )

    @api.model_create_multi
    def create(self,vals_list):
        """Generate sequence for book records"""
        print('vals_list',vals_list)
        for vals in vals_list:
            if vals.get('name','New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('library.books') or 'New'
        return super(LibraryBooks,self).create(vals_list)

    @api.constrains('book_isbn')
    def _validate_isbn(self):
        """ISBN validation
        --------------------
        raises ValidationError if
        the ISBN does not contain
        exactly 13 digits"""
        for rec in self:
            if len(rec.book_isbn) != 13:
                raise ValidationError("ISBN must contain 13 digits")


    def action_make_available(self):
        print(self)
        if self.book_status == 'coming_soon':
            self.book_status = 'available'

