# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Mate Elearning",
    'summary': """ Elearning """,
    'description': """""",
    'sequence': '-100',
    'version': '0.1',
    'depends': ['website_slides', 'sale'],
    'data': [
        'views/dashboard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mate_elearning/static/src/css/dashboard_view.scss',
            'mate_elearning/static/src/js/dashboard_view.js',

            'mate_elearning/static/src/lib/chart/js/highcharts.js',
            'mate_elearning/static/src/lib/chart/css/chart_view.scss',

            'mate_elearning/static/src/lib/calendar/css/date.scss',
            'mate_elearning/static/src/lib/calendar/css/datestyle.scss.css',
            'mate_elearning/static/src/lib/calendar/js/date.js',

        ],
        'web.assets_qweb': [
            'mate_elearning/static/src/xml/dashboard_view.xml',
        ],
    },
    'images': [
    ],
    'application': True,
}
