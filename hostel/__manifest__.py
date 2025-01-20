# -*- coding: utf-8 -*-
{
    'name': 'Hostel',
    'version': '18.0.1.0.0',
    'summary': 'Manage hostel rooms and students',
    'sequence': 10,
    'description': """"
Hostel Management
====================
The easy to use hostel management system which allows to add students and allocate them to specific rooms.
""",
    'category': 'Human Resources/Hostel',
    'website': '',
    'depends': ['base', 'mail', 'product', 'account', 'base_automation'],
    'data': [
        'data/hostel_sequence_data.xml',
        'data/hostel_rent_product_data.xml',
        'data/ir_cron_data.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/record_rule.xml',
        'views/hostel_room_views.xml',
        'views/hostel_student_views.xml',
        'views/hostel_facility_views.xml',
        'views/leave_request.xml',
        'views/hostel_invoice_views.xml',
        'views/cleaning_service_views.xml',
        'views/hostel_menu.xml',

    ],
    'demo': [
        'data/hostel_facility_data.xml'],
    'installable': True,
    'application': "True",
    'author': 'Fadil',
    'license': 'LGPL-3',

}
