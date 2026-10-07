# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    meeting_count = fields.Integer(
        string='Meeting Count',
        compute='_compute_meeting_count',

    )

    def _compute_meeting_count(self):
        print('_compute_meeting_count')
        self.meeting_count = self.env['mail.activity'].search_count([
            ('activity_type_id','=',self.env['mail.activity.type'].search([('name','=','Meeting')])),
            ('res_model','=','crm.lead'),
            ('res_name','=',self.name),
            ('active','=',False)
        ])

    def action_set_won_rainbowman(self):
        is_group_user = self.env.user.has_group('sales_team.group_sale_manager')
        if is_group_user:
            return super().action_set_won_rainbowman()
        if self.meeting_count == 0:
            raise ValidationError(f"{self.partner_id.name} has currently completed 0 meetings or any other activities to be converted to an Opportunity. Please schedule a new meeting or complete already scheduled meetings/activities to proceed")
        return super().action_set_won_rainbowman()