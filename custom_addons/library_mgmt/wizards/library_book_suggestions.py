# -*- coding: utf-8 -*-
from odoo import api,fields,models


class LibraryBookSuggestions(models.TransientModel):
    _name = 'library.book.suggestions'
    _description = 'Library Book Suggestions Wizard'

    checkout_id = fields.Many2one('library.checkouts')
    suggestion_ids = fields.Many2many('library.books')
    # recommend_reason = fields.Selection([('same_author',"Other Works by the Author"),('same_genre',"Same Genre"),('popular',"Popular Reads")])


    def add_books(self):
        """Add suggested books to checkout_lines"""
        checkout_id = self.env['library.checkouts'].browse(self.checkout_id).id
        print(checkout_id.id)

        genre =[]
        for rec in self.suggestion_ids.book_genre_ids:
            genre.append(rec.id)
        self.checkout_id.update({
            'checkout_lines_ids': [
                fields.Command.create({
                    'book_id': res.id,
                }) for res in self.suggestion_ids
            ]
        })
        for book in self.checkout_id.checkout_lines_ids:
            book.book_id.write({
                'book_status': 'unavailable',
            })
