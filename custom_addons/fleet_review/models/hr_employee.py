# -*- coding: utf-8 -*-
from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_available_technician = fields.Boolean(
        string='Technician Is Available?',
    )

    vehicle_ids = fields.Many2many(
        'fleet.vehicle',
        domain=[
            ('service_blocked','!=',True),
        ]
    )