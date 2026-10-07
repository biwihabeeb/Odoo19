# -*- coding: utf-8 -*-
{
    'name': "Weather Notification",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'depends': [
        "web",
        "base",
    ],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            "weather_notification/static/src/js/weather_popup_icon.js",
            "weather_notification/static/src/xml/weather_popup_icon.xml",
        ],
    },
    'data': [
        "views/res_config_settings_views.xml",
    ],
}