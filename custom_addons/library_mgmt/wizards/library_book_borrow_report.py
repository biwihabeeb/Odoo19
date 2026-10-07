# -*- coding: utf-8 -*-
from email.policy import default
import io
import json
from odoo import fields, models
from odoo.tools import date_utils, json_default

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class LibraryBookBorrowReport(models.TransientModel):
    _name = "library.book.borrow.report"

    member_id = fields.Many2one(
        'res.partner',
        string="Member ID",
    )
    book_id = fields.Many2one(
        'library.books'
    )
    author_id = fields.Many2one(
        'library.authors',
        string="Author",
    )
    checkout_date = fields.Date(
        string="Checkout Date",
    )

    return_date = fields.Date(
        string="Return Date",
    )

    publisher_id = fields.Many2one(
        'library.publishers',
    )

    genre_id = fields.Many2one(
        'library.genres'
    )

    sort = fields.Selection(
        [
            ('checkout', 'Checkout date'),
            ('due', 'Expected Return Date')
        ],
        string="Sort by",
        default=False
    )

    def print_borrow_report(self):
        query = """
            select
                c.name as reference_id,
                r.name as member_name,
                b.book_title as title,
				a.name as author,
				i.name as language,
				p.name as publisher,
				g.name as genre,
				c.checkout_date,
				c.checkout_returned
            from
                library_checkouts c
			inner join
				res_partner r on r.id = c.checkout_member_name_id
			inner join
				library_checkoutlines l on l.checkout_id = c.id
			inner join
				library_books b on b.id = l.book_id
			inner join
			    res_lang i on i.id = b.book_language_id
			inner join
				library_authors a on a.id = b.book_author_id
			inner join
				library_publishers p on p.id = b.book_publisher_id
			inner join
				library_books_library_genres_rel e on e.library_books_id = b.id
			inner join
				library_genres g on g.id = e.library_genres_id
            """

        condition_str = []
        condition_arg = []

        if self.member_id:
            condition_str.append("""r.id=%s""")
            condition_arg.append(self.member_id.id)
        if self.book_id:
            condition_str.append("""b.id=%s""")
            condition_arg.append(self.book_id.id)
        if self.author_id:
            condition_str.append("""a.id=%s""")
            condition_arg.append(self.author_id.id)
        if self.publisher_id:
            condition_str.append("""p.id=%s""")
            condition_arg.append(self.publisher_id.id)
        if self.genre_id:
            condition_str.append("""g.id=%s""")
            condition_arg.append(self.genre_id.id)
        if self.checkout_date:
            condition_str.append("""checkout_date='%s'""")
            condition_arg.append(self.checkout_date)
        if self.return_date:
            condition_str.append("""return_date='%s'""")
            condition_arg.append(self.return_date)

        if self.sort:
            if self.sort == 'checkout':
                if condition_str and condition_arg:
                    query += """where """ + """ and """.join(condition_str) + """ order by c.checkout_date""" + """;"""
                    self.env.cr.execute(query % tuple(condition_arg))
                else:
                    query += """ order by c.checkout_date""" + """;"""
                    self.env.cr.execute(query)
            elif self.sort == 'due':
                if condition_str and condition_arg:
                    query += """where """ + """ and """.join(condition_str) + """ order by c.checkout_return_due""" + """;"""
                    self.env.cr.execute(query % tuple(condition_arg))
                else:
                    query += """ order by c.checkout_return_due""" + """;"""
                    self.env.cr.execute(query)
        else:
            if condition_str and condition_arg:
                query += """where """ + """ and """.join(condition_str) + """;"""
                self.env.cr.execute(query % tuple(condition_arg))
            else:
                query += """;"""
                self.env.cr.execute(query)


        recs = self.env.cr.dictfetchall()
        print('recs :',recs)
        data = {
            'member': self.member_id.name,
            'book': self.book_id.book_title,
            'author': self.author_id.name,
            'publisher': self.publisher_id.name,
            'genre': self.genre_id.name,
            'checkout': self.checkout_date,
            'return_date': self.return_date,
            'report': recs,
        }
        # print(self.env.ref('library_mgmt.action_library_book_borrow_report').report_action(None,data = data))
        return self.env.ref('library_mgmt.action_library_book_borrow_report').report_action(None,data = data)

    def print_borrow_report_xlsx(self):
        data = {
            'member': self.member_id.name,
            'book': self.book_id.book_title,
            'author': self.author_id.name,
            'publisher': self.publisher_id.name,
            'genre': self.genre_id.name,
            'checkout': self.checkout_date,
            'return_date': self.return_date,
        }
        print('running')
        return {
            'type': "ir.actions.report",
            'data': {
                'model': 'library.book.borrow.report',
                'options': json.dumps(data, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Library Management Report',
            },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        print('get report')
        query = """
            select
	            b.name as book_reference_id,
	            b.book_title,
	            b.book_isbn as isbn,
	            i.name as language_,
	            a.name as author,
	            g.name as genre,
	            p.name as publisher,
	            c.name checkout_refernce_id,
	            c.checkout_date,
	            c.checkout_returned
            from
	            library_checkouts c
	        inner join
				res_partner r on r.id = c.checkout_member_name_id
            inner join
	            library_checkoutlines l on l.checkout_id = c.id
            inner join
	            library_books b on b.id = l.book_id
            inner join
	            res_lang i on i.id = b.book_language_id
            inner join
	            library_authors a on a.id = b.book_author_id
            inner join
	            library_publishers p on p.id = b.book_publisher_id
            inner join
	            library_books_library_genres_rel e on e.library_books_id = b.id
            inner join
	            library_genres g on g.id = e.library_genres_id
        """
        #FILTER
        condition_str = []
        condition_arg = []
        # print('is self available', data['member'])
        if data['member']:
            condition_str.append("""r.name='%s'""")
            condition_arg.append(data['member'])
        if data['book']:
            condition_str.append("""b.book_title='%s'""")
            condition_arg.append(data['book'])
        if data['author']:
            condition_str.append("""a.name='%s'""")
            condition_arg.append(data['author'])
        if data['publisher']:
            condition_str.append("""p.name='%s'""")
            condition_arg.append(data['publisher'])
        if data['genre']:
            condition_str.append("""g.name='%s'""")
            condition_arg.append(data['genre'])
        if data['checkout']:
            condition_str.append("""checkout_date='%s'""")
            condition_arg.append(data['checkout'])
        if data['return_date']:
            condition_str.append("""return_date='%s'""")
            condition_arg.append(data['return_date'])

        #SORT
        if self.sort:
            if self.sort == 'checkout':
                if condition_str and condition_arg:
                    query += """where """ + """ and """.join(condition_str) + """ order by c.checkout_date""" + """;"""
                    self.env.cr.execute(query % tuple(condition_arg))
                else:
                    query += """ order by c.checkout_date""" + """;"""
                    self.env.cr.execute(query)
            elif self.sort == 'due':
                if condition_str and condition_arg:
                    query += """where """ + """ and """.join(condition_str) + """ order by c.checkout_return_due""" + """;"""
                    self.env.cr.execute(query % tuple(condition_arg))
                else:
                    query += """ order by c.checkout_return_due""" + """;"""
                    self.env.cr.execute(query)
        else:
            if condition_str and condition_arg:
                query += """where """ + """ and """.join(condition_str) + """;"""
                self.env.cr.execute(query % tuple(condition_arg))
            else:
                query += """;"""
                self.env.cr.execute(query)

        # print('filter data:',data)
        docs = self.env.cr.dictfetchall()
        print('fetched data:',docs)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{'in_memory':True})
        sheet = workbook.add_worksheet('docs')
        sheet.set_column('A:M',15)
        head = workbook.add_format(
            {
                'bold': True,
                'font_size': 30,
                'align': 'center',
            }
        )
        filter_by = workbook.add_format({
            'bold': True,
            'font_size': 12,
        })
        filter_field = workbook.add_format({
            'font_size': 12,
        })
        table_headers = workbook.add_format({
            'bold': True,
            'font_size': 12,
        })

        print(data)

        sheet.merge_range('A1:I4','Library Management Report',head)
        headers = ['Book Refence Id',
                   'Book Title',
                   'ISBN','Language',
                   'Author',
                   'Genre',
                   'Publisher',
                   'Checkout Reference Id',
                   'Checkout date',
                   'Returned date',
                   ]

        if data['book']:
            headers.remove('Book Title')
        if data['author']:
            headers.remove('Author')
        if data['publisher']:
            headers.remove('Publisher')
        if data['genre']:
            headers.remove('Genre')
        if data['checkout']:
            headers.remove('Checkout date')
        if data['return_date']:
            headers.remove('Returned date')



        filters = ''
        count_filters = 0
        for key in data:
            if data[key]:
                # sheet.merge_range(f'A{7+count_filters}:AMJ{7+count_filters}',key+': '+data[key],filter_field)
                count_filters += 1
                if data['member']:
                    filters += f'Member name: {data['member']}\n'
                if data['book']:
                    filters += f'Book title: {data['book']}\n'
                if data['author']:
                    filters += f'Author: {data['author']}\n'
                if data['publisher']:
                    filters += f'Publisher: {data['publisher']}\n'
                if data['genre']:
                    filters += f'Genre: {data['genre']}\n'
                if data['checkout']:
                    filters += f'Checkout date: {data['checkout']}\n'
                if data['return_date']:
                    filters += f'Returned date: {data['return_date']}\n'
        print('filters: ',filters)
        if count_filters > 0:
            sheet.set_row(5,34)
            sheet.merge_range(f'A6:AMJ6', 'Applied Filters:\n', filter_by)
            sheet.merge_range(f'A7:AMJ{7+count_filters}',filters,filter_field)
        print('count_filters:',count_filters)
        # for key in docs[0]:
        #     headers.append(key)
        # print('headers:',headers)

        if count_filters == 0:
            sheet.write_row('A6', tuple(headers), table_headers)
            row = 6
        else:
            sheet.write_row(f'A{8+count_filters}', tuple(headers), table_headers)
            row = 8 + count_filters
        col = 0
        for doc in docs:
            rec = []
            for key in doc:
                if key in ['checkout_date','checkout_returned'] and doc[key]:
                    rec.append(doc[key].strftime('%Y-%m-%d'))
                else:
                    rec.append(doc[key])
            for k in data:
                if data[k] and data[k] in rec:
                    rec.remove(data[k])
            sheet.write_row(row,col,tuple(rec))
            row += 1

        # print('type class of response: ',type(response))
        # print('Output: ',output.getvalue())
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()



        # HEADER: reference_id, ISBN, name, language, author, checkout date, return date, category, genre

