# -*- coding: utf-8 -*-
import json

from docutils.utils.smartquotes import options

from odoo import http
from odoo.http import content_disposition, request, serialize_exception
from odoo.tools import html_escape

class XLSXReportController(http.Controller):

    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], crsf=False)
    def get_report_xlsx(self, model, options, output_format, report_name):
        print('controller working.')
        report_obj = request.env[model].with_user(request.session.uid)
        options = json.loads(options)
        token = 'dummy-api-expects-a-token'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition(report_name+'.xlsx')),
                    ]
                )
                report_obj.get_xlsx_report(options,response)
            # print('Controller returns type of response: ',type(response))
            response.set_cookie('fileToken',token)
            return response
        except Exception as e:
            se = serialize_exception(e)
            error =  {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se,
            }
            return request.make_response(html_escape(json.dumps(error)))