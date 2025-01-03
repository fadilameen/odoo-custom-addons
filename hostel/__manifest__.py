# -*- coding: utf-8 -*-

{
    'name': 'Hostel',
    'version': '18.0.1.0.0',
    'summary': 'Manage hostel rooms and students',
    'sequence': 1,
    'description': """"
Hostel Management
====================
The easy to use hostel management system which allows to add students and allocate them to specific rooms.
""",
    'category': 'Human Resources/Hostel',
    'website': '',
    'depends': ['base', 'mail', ],
    'data': [
        'data/hostel_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/hostel_room_views.xml',
        'views/hostel_student_views.xml',
        'views/hostel_facilities_views.xml',
        'views/hostel_menu.xml',

    ],
    'demo': [
        'data/hostel_facilities_data.xml'],
    'installable': True,
    'application': "True",
    'author': 'Fadil',
    'license': 'LGPL-3',

}
