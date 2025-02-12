# -*- coding: utf-8 -*-
{
    'name': 'Bill of Materials in Cart',
    'version': '18.0.1.0.0',
    'summary': 'Display bill of materials in cart in website',
    'sequence': 1,
    'description': """"
Bill of Materials in Cart
====================
To display bill of materials in website cart.
""",
    # 'category': 'Sales',
    # 'website': '',
    'depends': ['website_sale', 'mrp'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/website_sale_cart_views.xml',
        #          'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': "False",

    'author': 'Fadil',
    'license': 'LGPL-3',

}
