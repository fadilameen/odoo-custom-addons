{
    'name': "Clinic",
    'application': "True",
    'depends': ['base', 'hr', 'hr_hourly_cost', ],
    'data': [
        'security/ir.model.access.csv',
        'views/op_ticket_sequence.xml',
        'views/patient_registration.xml',
        'views/op_ticket.xml',
        'views/clinic_consultation.xml',
        'views/clinic_prescription.xml',
        'views/clinic_menu.xml',

    ]
}
