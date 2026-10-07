# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields,models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Configuration Settings'

    max_borrow_days = fields.Integer(
        string="Max Borrowing Days",
        config_parameter = 'library_mgmt.max_borrow_days',
        default = 14
    )

    reminder_days = fields.Integer(
        string = "Reminder Days",
        config_parameter = 'library_mgmt.reminder_days',
        default = 2
    )

    penalty_per_hour = fields.Float(
        string = "Penalty per Hour",
        config_parameter = 'library_mgmt.penalty_per_hour',
        default = 0.5
    )

    max_borrow_number = fields.Integer(
        string="Max Number of Books",
        config_parameter = 'library_mgmt.max_borrow_number',
        default = 1
    )

    max_allowed_late_returns = fields.Integer(
        string="Maximum Late Returns Allowed",
        config_parameter = 'library_mgmt.max_allowed_late_returns',
        default = 10
    )