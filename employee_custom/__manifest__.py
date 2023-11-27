# -*- coding: utf-8 -*-
{
    'name': "employee customized",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

   
    'category': 'Mitur/employeeCustom',
    'version': '0.1',
    'depends': ['base','hr','mail','hr_skills'],
    'application': False,  
    # always loaded
    'data': [  
        'security/ir.model.access.csv',     
        'views/custom_employee.xml',
        'views/tipo_empleado_views.xml',
        'views/custom_employee.xml',
        'views/custom_menu_config_employee.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
