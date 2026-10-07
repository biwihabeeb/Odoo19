# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime, date

class HrDailyAbsentees(models.Model):
    _name = 'hr.daily.absentees'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
    )
    working_day = fields.Datetime(
        string='Attendance Date',
    )


    @api.model
    def get_daily_absentees(self):
        present_ids = self.env['hr.attendance'].search([
            ('date','=',date.today())
        ])
        absentees = self.env['hr.employee'].search([]).filtered(lambda employee: employee.id not in present_ids.mapped('employee_id').ids)

        for absentee in absentees:
            self.create({
                'employee_id': absentee.id,
                'working_day': datetime.today(),
            })


