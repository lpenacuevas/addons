
# -*- coding: utf-8 -*-
{
    'name': "staffaction",

    'summary': """
       Gestionar todas las acciones que se realizan en la institucion""",

    'description': """
        Contiene un mantenimiento de los tipos de acciones y detalles
    """,

    'author': "Mitur",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Mitur/staffaction',
    'version': '0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/staff_action_group_admin.xml',
        'data/staff_action_stage.xml',
        'data/type_action_staff.xml',
        'views/staff_menu.xml',
        'views/staff_views.xml',
        'views/applicant_action_view.xml',
        'reports/staffaction_report.xml'
    ],
    "application": True,
    #installable
    #auto_install
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
}
