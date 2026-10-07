# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import timedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def send_contract_expiry_reminder_mail(self):
        relative_delta = int(self.env['ir.config_parameter'].sudo().get_param("employee_contract_expiry_email.contract_expiration_due"))
        employee_contract_expiring = self.env['hr.employee'].search([
            ('contract_date_start', '!=', False),
            ('contract_date_start', '<', fields.Date.today()),
            ('contract_date_end', '=', fields.Date.today() + timedelta(days=relative_delta))
        ])
        template = self.env.ref("employee_contract_expiry_email.email_template_employee_contract_expiry_reminder")
        for employee in employee_contract_expiring:
            template.send_mail(employee.id,force_send=True)
