# -*- coding: utf-8 -*-
{
    'name': 'Slider Widget',
    'version': '18.0.1.0.0',
    'summary': 'Slider Widget',
    'description': """"
Slider Widget
""",
    'depends': ['product'],

    'assets': {
        'web.assets_backend': [
            'slider_widget/static/src/xml/slider.xml',
            'slider_widget/static/src/js/slider.js',
        ],
    },
    'data': [
        'views/product_product_views.xml',
    ],
    'author': 'Fadil',
    'license': 'LGPL-3',

}
