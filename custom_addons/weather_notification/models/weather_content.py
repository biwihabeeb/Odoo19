# -*- coding: utf-8 -*-
from odoo import api, models
import requests

class WeatherContent(models.Model):
    _name = 'weather.content'
    _description = 'Weather Content'

    @api.model
    def get_weather_content(self):
        # print('GET WEATHER CONTENT')
        try:
            param_q = self.env['ir.config_parameter'].sudo().get_param('weather_notification.weather_config')
            if param_q == 'loc':
                region_q = self.env['ir.config_parameter'].sudo().get_param('weather_notification.region')
                response = requests.get(f"http://api.weatherapi.com/v1/current.json?key=f5421322cbe243fc97a31710261908&q={region_q}&aqi=no")
            elif param_q == 'lat_long':
                latitude = self.env['ir.config_parameter'].sudo().get_param('weather_notification.latitude')
                longitude = self.env['ir.config_parameter'].sudo().get_param('weather_notification.longitude')
                response = requests.get(
                    f"http://api.weatherapi.com/v1/current.json?key=f5421322cbe243fc97a31710261908&q={latitude},{longitude}&aqi=no")
            response.raise_for_status()
            data = response.json()
            # print('WEATHER DATA....', data)

            if data:
                return {
                    'location': [data['location']['name'], data['location']['region'], data['location']['country']],
                    'timezone': data['location']['tz_id'],
                    'temp_c': data['current']['temp_c'],
                    'temp_f': data['current']['temp_f'],
                    'condition': data['current']['condition']['text'],
                    'wind_mph': data['current']['wind_mph'],
                    'wind_kph': data['current']['wind_kph'],
                    'wind_dir': data['current']['wind_dir'],
                    'icon': data['current']['condition']['icon']
                }
        except:
            return {}


