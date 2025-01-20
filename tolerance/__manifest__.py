# -*- coding: utf-8 -*-
{
    'name': 'Tolerance',
    'version': '18.0.1.0.0',
    'summary': 'Manage tolerance for various customers',
    'sequence': 1,
    'description': """"
Tolerance
====================
Helps to manage tolerance in quantities for various products.
""",
    'category': 'Sales',
    'website': '',
    'depends': ['base', 'sale_management', ],
    'data': ['views/res_partner_views.xml',
             'views/sale_order_line_views.xml',
             ],
    'installable': True,
    'application': "False",

    'author': 'Fadil',
    'license': 'LGPL-3',

}
