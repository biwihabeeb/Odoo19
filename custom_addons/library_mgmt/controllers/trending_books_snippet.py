# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class TrendingBooksSnippet(http.Controller):
    @http.route(['/get_trending_books'], type='jsonrpc', auth='public', website=True)
    def get_trending_books(self, **kw):
        # print('*'*100)
        trending_books = request.env['library.books'].sudo().search_read([], fields=['id','book_title','book_cover'], order='book_borrow_count desc', limit=10)
        # borrow_count = request.env['library.books'].sudo().search([('book_title','=','test-book-14')])
        # print(borrow_count.mapped('book_title'),borrow_count.mapped('book_borrow_count'))
        # print(trending_books)
        values = {
            'books': trending_books,
        }
        return values