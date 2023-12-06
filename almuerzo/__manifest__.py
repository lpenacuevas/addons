# -*- coding: utf-8 -*-
{
    'name': "Almuerzo",

    'summary': """
        A module to manage lunch for the staff of the Ministerio de Turismo de la República Dominicana""",

    'author': "Mitur",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Mitur/Almuerzo',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/almuerzo_menu.xml',
        'views/almuerzo_views.xml',
        'views/tipo_persona_views.xml'
    ],

    "application": True,

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
