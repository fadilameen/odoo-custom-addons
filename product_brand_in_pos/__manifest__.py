# -*- coding: utf-8 -*-
{
    'name': "Product Brand in POS",
    'version': '18.0.1.0.0',
    'summary': 'Product Brand in POS',
    'sequence': 1,
    'description': """"
Product Brand in POS
====================
Product Brand in POS.
""",
    'category': 'Point of Sale',
    'website': '',
    'depends': ['point_of_sale', 'product'],
    'data': [
        'views/product_product_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'product_brand_in_pos/static/src/xml/pos_order_line_views.xml',
            'product_brand_in_pos/static/src/js/pos_store.js',
        ],
    },
    'installable': True,
    'author': 'Fadil',
    'license': 'LGPL-3',
}
