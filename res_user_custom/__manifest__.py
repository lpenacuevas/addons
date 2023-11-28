# -*- coding: utf-8 -*-

{
    'name': "res_user_custom",
    'sequence': -1,

    'summary':
        """Relacion Empleados-Usuarios""",

    'description': """
        Cambia la relacion entre el usuario y el contacto y la realiza con empleado
    """,

    'author': "Mitur",
    'website': "http://www.yourcompany.com",


    'category': 'Mitur/customized',
    'version': '0.1.0',
    'depends': ['base', 'hr'],
    'application': False,
    # always loa ded
    'data': [
        'security/ir.model.access.csv',  # seguridad del modelo
        'views/res_user_custom.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
