# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64

class WebsiteBookDonationFormController(http.Controller):
    @http.route(['/website/book_donate/form'], type='http', auth="public", website=True)
    def donate_book_form(self, **kw):
        genres = self.env['library.genres'].sudo().search([])
        values = {
            'genres': genres,
        }
        return request.render('library_mgmt.book_donation_form_template', values)

    @http.route(['/website/book_donate/create'], type='http', auth="public",methods=['POST'], website=True, csrf=True)
    def create_book_record(self, **post):
        print('create book record')
        book_cover = post.get('attachment')
        book_image_content = book_cover.read()
        base64_book_cover = base64.b64encode(book_image_content).decode()

        print('Cover: ',base64_book_cover)
        author_id = self.env['library.authors'].sudo().search([
            ('name', '=', post.get('author_name'))
        ])
        if not author_id:
            author_id = self.env['library.authors'].sudo().create({
                'name': post.get('author_name')
            })
        print(author_id)

        publisher_id = self.env['library.publishers'].sudo().search([
            ('name', '=', post.get('publisher'))
        ])
        if not publisher_id:
            publisher_id = self.env['library.publishers'].sudo().create({
                'name': post.get('publisher')
            })

        genre_ids = self.env['library.genres'].sudo().search([
            ('id', '=', post.get('genres'))
        ])

        request.env['library.books'].sudo().create({
            'book_title': post.get('book_title'),
            'book_author_id': author_id.id,
            'book_isbn': post.get('isbn'),
            'book_publisher_id': publisher_id.id,
            'book_status': 'coming_soon',
            'book_genre_ids': genre_ids.ids,
            'book_cover': base64_book_cover,
        })
        return request.render('library_mgmt.donation_success_template')

    @http.route(['/my/book_donations'], type='http', auth="public", website=True)
    def get_book_records(self, **kw):
        print('user:',self.env.user.id)
        records = request.env['library.books'].sudo().search([
            ('book_status', '=', 'coming_soon'),
            ('create_uid','=', self.env.user.id),
        ])
        print('REFERENCE ID\tBOOK TITLE\tAUTHOR NAME\tBOOK ISBN\tBOOK PUBLISHER')
        for rec in records:
            print(rec.name,rec.book_title,rec.book_author_id.name,rec.book_isbn,rec.book_publisher_id.name,sep='\t')
        print(records)
        data = {
            'records': records,
        }
        return request.render('library_mgmt.portal_my_book_donation_records',data)

    @http.route(['/my/book_donations/<int:book_id>'], type='http', auth="public", website=True)
    def get_portal_book_record(self, book_id, **kw):
        record = request.env['library.books'].sudo().search([
            ('id','=', book_id),
        ])

        values = {
            'record': record,
            # 'book_cover': book_cover,
            # 'genre': genre,
            # 'book_cover': base64_book_cover,
        }
        return request.render('library_mgmt.portal_my_book_donation_record',values)

