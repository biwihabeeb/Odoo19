# -*- coding: utf-8 -*-
from odoo import api, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_dashboard_context(self):
        print('SEARCH CRM LEAD')
        leads_count = self.search_count([
            ('type', '=', 'lead'),
            ('user_id', '=', self.env.user.id),
        ])
        opportunities_count = self.search_count([
            ('type', '=', 'opportunity'),
            ('user_id', '=', self.env.user.id),
        ])
        currency = self.env.company.currency_id.symbol
        expected_revenue = self.search([
            ('user_id','=',self.env.user.id)
        ]).mapped('expected_revenue')
        earned_revenue = self.env['account.move'].search([
            ('invoice_user_id','=',self.env.user.id),
        ]).mapped('amount_total_in_currency_signed')

        won = self.search_count([
            ('won_status', '=', 'won'),
            ('user_id','=',self.env.user.id),
        ])
        total = self.search_count([
            ('user_id','=',self.env.user.id),
            # ('won_status', '=', 'lost'),
        ])
        lost = self.search_count([
            ('won_status','=','lost'),
            ('active','=',False),
        ])
        activity_recs = self.env['mail.activity'].search_read(
            [
                ('res_model_id','=',765),
            ],
            fields=['display_name','activity_type_id'],
        )
        # print(activity_recs)

        query1 = """
            select 
                date_trunc('month', create_date) as month, 
                count(*)
            from 
                crm_lead c 
            where 
                c.active = true 
            and 
                c.type = 'lead' 
            group by 
                date_trunc('month', create_date);
        """
        dict_month = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        self.env.cr.execute(query1)
        leads_by_month = self.env.cr.dictfetchall()
        monthly_leads = []
        for rec in leads_by_month:
            key = rec['month'].month
            monthly_leads.append({'month': dict_month[key], 'leads': rec['count'], 'key': key})

        query2 = """
            select 
                m.name as medium, 
                count(*) as leads 
            from 
                crm_lead c 
            inner join 
                utm_medium m 
            on 
                m.id = c.medium_id 
            group by 
                m.name;
        """
        self.env.cr.execute(query2)
        leads_medium = self.env.cr.dictfetchall()
        # print(leads_medium)

        query3 = """
            select 
                c.name as campaign, 
                count(*) as leads 
            from 
                crm_lead l 
            inner join 
                utm_campaign c 
            on 
                c.id = l.campaign_id 
            group by 
            c.name; 
        """
        self.env.cr.execute(query3)
        leads_by_campaign = self.env.cr.dictfetchall()
        # print(leads_by_campaign)

        lost_leads = self.search_read([
            ('won_status','=','lost'),
            ('active','=',False),
        ],
            fields=['name','lost_reason_id'],
        )
        print(lost_leads)
        for lead in lost_leads:
            if lead['lost_reason_id'] == False:
                lead['lost_reason'] = 'unknown reason'
            else:
                lead['lost_reason'] = lead['lost_reason_id'][1]
        print(lost_leads)

        query4 = """
            select 
                a.name as activity_type, 
                count(*) as activities 
            from 
                mail_activity m 
            inner join 
                mail_activity_type a 
            on 
                a.id = m.activity_type_id 
            where 
                m.res_model_id = 765 
            group by 
                a.name;
        """
        self.env.cr.execute(query4)
        activities = self.env.cr.dictfetchall()
        # print(activities)


        return {
            'leads_count': leads_count,
            'opportunities': opportunities_count,
            'currency': currency,
            'expected_revenue': sum(expected_revenue),
            'earned_revenue': sum(earned_revenue),
            'win_ratio': round((won / total) * 100, 2),
            'activities': activities,
            'leads_by_month': sorted(monthly_leads, key=lambda x: x['key']),
            'leads_by_medium': leads_medium,
            'leads_by_campaign': leads_by_campaign,
            'lost_leads': lost_leads,
        }