# -*- coding: utf-8 -*-
from odoo import fields, models, api

class MailActivity(models.Model):
    _inherit = 'mail.activity'


    def _action_done(self, feedback = False, attachment_ids = None):
        res = super()._action_done(feedback, attachment_ids)
        if self.calendar_event_id:
            task = self.env['project.task'].browse(self.res_id)
            print(task)
            timesheet = self.env['account.analytic.line'].create({
                'employee_id': self.env['hr.employee'].search([('name','=',self.env.user.name)]).id,
                'name': self.summary,
                'task_id': task.id,
                'project_id': task.project_id.id,
                # 'unit_amount': (self.calendar_event_id.stop_date - self.calendar_event_id.start_date).hours if self.calendar_event_id.stop_date and self.calendar_event_id.start_date else 0,
            })
        return res


