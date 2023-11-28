# -*- coding: utf-8 -*-
{
    'name': "horas labor",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

   
    'category': 'Mitur/horas_labor',
    'version': '0.1',
    'depends': ['base','hr','mail'],
    'application': False,  
    # always loaded
    'data': [  
        'security/ir.model.access.csv',     
        'views/calendar_attendance_view_extended.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
