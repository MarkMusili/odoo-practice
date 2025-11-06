{
    "name": "Hosptial Dashboard",
    "description": "A dashboard for the Hospital Management system",
    "author": "Mark Musili",
    "licence": "LGPL-3",
    "depends": ['hospital'],
    "data": [
        'views/views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'hospital_dashboard/static/src/**/*',
        ],
    },
    "installable": True,
    "application": True,
}