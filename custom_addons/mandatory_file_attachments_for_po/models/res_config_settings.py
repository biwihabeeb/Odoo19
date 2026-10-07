# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields, models
from odoo.tools import config


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    attachment_required = fields.Boolean(
        string="Attachment Required",
        config_parameter="purchase.attachment_required",
        default=False
    )