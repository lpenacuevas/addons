
# -*- coding: utf-8 -*-
{
    'name': "Vistitantes ",

    'summary': """
       Gestionar las entradas de los visitantes al mitur """,

    'description': """
        crea label de entrada y conecta con el lector
    """,

    'author': "Mitur",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Mitur/Visitantes',
    'version': '0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_jce.xml',
        'views/visitantes_menu.xml',
        'views/visitantes_view.xml',
    ],
    "application": True,
    #installable
    #auto_install
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
}
