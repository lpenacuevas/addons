
# -*- coding: utf-8 -*-
{
    'name': "localidades",

    'summary': """
       Direccion para los departamentos con diferentes tipos de localidades o sucursales""",

    'description': """
        Mantenimiento de localidades
    """,

    'author': "Mitur",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Mitur/Localidades',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/localidad_menu.xml',
        'views/localidad_views.xml', 
        'views/pisos_view.xml',
             
    ],
    "application": True,
    #installable
    #auto_install
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
}
