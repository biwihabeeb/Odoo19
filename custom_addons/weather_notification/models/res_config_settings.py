# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    region = fields.Char(
        config_parameter='weather_notification.region',
    )
    weather_config = fields.Selection(
        [
            ('lat_long','By Latitude and Longitude'),
            ('loc','By Region'),

         ],
        string='Configure Weather Location',
        config_parameter='weather_notification.weather_config',
    )
    latitude = fields.Float(
        string='Latitude',
        config_parameter='weather_notification.latitude',
    )
    longitude = fields.Float(
        string='Longitude',
        config_parameter='weather_notification.longitude',
    )