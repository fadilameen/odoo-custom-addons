# -*- coding: utf-8 -*-
{
    'name': 'POS Category Wise Discount',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Apply category-wise discounts in POS',
    'depends': ['point_of_sale'],
    'data': [
        'views/res_config_settings_views.xml',  # Add your XML views here
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_category_wise_discount/static/src/xml/pos_order_line_views.xml',
            'pos_category_wise_discount/static/src/js/pos_order_line.js',
        ],
    },

    'installable': True,
    'application': True,
}
