# -*- coding: utf-8 -*-
{
    'name': 'Day Wise Attendance',
    'version': '18.0.1.0.0',
    'summary': 'Manage daily absentees',
    'sequence': 1,
    'description': """"
Day wise attendance
====================
The easy to use absentees management system
""",
    'category': 'Human Resources/Day Wise Attendance',
    'website': '',
    'depends': ['hr'],
    'data': ['data/ir_cron_data.xml',
             'security/ir.model.access.csv',
             'views/daily_absentee_views.xml',
             'views/day_wise_attendance_menu.xml',
             ],
    'installable': True,
    'application': "True",
    'author': 'Fadil',
    'license': 'LGPL-3',

}
