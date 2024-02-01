# -*- coding: utf-8 -*-
{
    'name': "Ausencias Custom",
    'summary':
        """Gestionar los registros de las ausencias del MITUR """,
    'description': """Este modulo permite adaptar el modulo base de Odoo de acuerdo con Mitur""",
    'author': "Mitur",
    'website': "http://www.mtiur.gob.do",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Mitur/Ausencias',
    'version': '0.1.5',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hr','hr_holidays'],

    # external dependencies
    'external_dependencies': {
    },

    # always loaded
    'data': [
        'views/hr_holidays_menus.xml',
        'views/hr_holidays_views.xml',


    ],
    "application": False,
    # installable
    # auto_install
    # only loaded in demonstration mode
}
