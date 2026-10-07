# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    force_approval = fields.Boolean(
        string="Force Validate?",
        group="group_hr_holidays_manager"
    )

    def action_approve(self,check_state=True):
        res = super().action_approve(check_state)
        overlapping_leave_count = self.search_count([
            ('employee_id', '!=', self.employee_id.id),
            ('department_id', '=', self.department_id.id),
            ('date_from', '<=', self.date_from),
            ('date_to', '>=', self.date_to),
            ('state', '=', 'validate'),
        ])

        overlapping_leave = self.search([
            ('employee_id', '!=', self.employee_id.id),
            ('department_id', '=', self.department_id.id),
            ('date_from','<=',self.date_from),
            ('date_to','>=',self.date_to),
            ('state','=','validate'),
        ])

        names = overlapping_leave.mapped('employee_id.name')
        print(names)

        print(self.env.ref("hr_holidays.group_hr_holidays_manager").id)

        department_employee_count = self.env['hr.employee'].search_count([
            ('department_id','=',self.department_id.id)
        ])
        # if self.force_approval:
        #     return res
        is_group_user = self.env.user.has_group("hr_holidays.group_hr_holidays_user")
        ts_group_user = self.env.user.has_group("hr_holidays.group_hr_holidays_manager")
        print(is_group_user,ts_group_user)
        # print(is_group_user)
        print(self.env.ref("hr_holidays.group_hr_holidays_user").name)
        # if is_group_user:
        if ts_group_user:
            return res
        if overlapping_leave_count >= department_employee_count/2:
            raise ValidationError("Over Half of the Department currently has leaves overlapping within the required dates."
                              "\nCurrently following employees are on leave:\n%s" % "\n".join(names))

        return res