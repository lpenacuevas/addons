# -*- coding: utf-8 -*-
{
    'name': "Control de Vacaciones",
    'summary': """
       Gestionar los registros de las vacaciones del MITUR """,
    'description': """
        crea label de entrada y conecta con el lector
    """,
    'author': "Mitur",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Mitur/Vacaciones',
    'version': '0.1.6',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hr', 'contacts', 'staffaction'],

    # external dependencies
    'external_dependencies': {
        'python': ['numpy'],
    },

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_vacation_menus.xml',
        'views/hr_vacation_views.xml',
        'wizard/hr_vacation_wizard.xml',
        'data/hr_vacation_stage.xml',
        'wizard/staff_planning_wizard.xml',
        'security/vacation_group_admin.xml',

    ],
    "application": True,
    # installable
    # auto_install
    # only loaded in demonstration mode
}
