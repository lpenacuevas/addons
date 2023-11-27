# -*- coding: utf-8 -*-
{
    'name': "departamento_localidad",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

   
    'category': 'Mitur/departamento_localidad',
    'version': '0.1',
    'depends': ['base','hr','mail','localidades'],
    'application': False, 
    "auto_install": True,
    # always loaded
    'data': [       
        'views/localidad_department_view_extended.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
