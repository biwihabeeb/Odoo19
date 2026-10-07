# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    contract_expiration_due = fields.Integer(
        config_parameter='employee_contract_expiry_email.contract_expiration_due',
        default = 7
    )