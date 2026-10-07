# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ReportLibraryBookBorrow(models.AbstractModel):
    _name = 'report.library_mgmt.library_book_borrow_report'

    @api.model
    def _get_report_values(self,docids,data=None):
        docs = self.env['library.book.borrow.report'].browse(docids)
        print('*'*40,docs)
        return {
            'doc_ids': docids,
            'doc_model': "library.book.borrow.report",
            'docs': docs,
            'data': data
        }