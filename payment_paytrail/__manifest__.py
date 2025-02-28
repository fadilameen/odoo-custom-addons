# -*- coding: utf-8 -*-
{
    'name': 'Payment Provider: Paytrail',
    'version': '18.0.1.0.0',
    'summary': 'An online payment provider for secure transactions.',
    'sequence': 10,
    'description': """
    Paytrail Payment Provider
    =========================
    An online payment provider facilitating secure transactions worldwide.
        """,
    'category': 'Accounting/Payment Providers',
    'depends': ['payment'],
    'data': [
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
    ],
    'icon': "/payment_paytrail/static/description/icon.svg",
    'application': False,
    'website': 'https://www.paytrail.com/en/',
    'author': 'Fadil Ameen',
    'license': 'LGPL-3',
}
