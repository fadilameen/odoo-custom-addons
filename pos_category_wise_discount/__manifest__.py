# -*- coding: utf-8 -*-
{
    'name': 'POS category wise discount',
    'depends': ['point_of_sale'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {'point_of_sale._assets_pos': [
        'pos_category_wise_discount/static/src/xml/pos_order_line_views.xml'
    ]}
}
