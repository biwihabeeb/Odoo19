# -*- coding: utf-8 -*-
from odoo import fields, models

class FleetServiceOrderChecklist(models.Model):
    _name = 'fleet.service.order.checklist'
    _rec_name = 'task_name'

    order_id = fields.Many2one(
        'fleet.service.order'
    )
    # — Many2one → fleet.service.order
    task_name = fields.Char(
        string='Name',
    )
    is_done = fields.Boolean(
        string='If Done?',
    )
    note = fields.Text(
        string='Notes',
    )
