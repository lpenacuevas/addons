# -*- coding: utf-8 -*-

{
    'name': "recruitment customized",
    'sequence': -1,

    'summary': """
        Grupo Ocupacional y viaticos por cargos""",

    'description': """
        Añade los grupos ocupacionales y tipo de viaticos por cargos
    """,

    'author': "Mitur",
    'website': "http://www.yourcompany.com",


    'category': 'Mitur/customized',
    'version': '0.1.0',
    'depends': ['base', 'hr', 'mail', 'hr_recruitment', 'staffaction'],
    'application': False,
    # always loaded
    'data': [
        'security/ir.model.access.csv',  # seguridad del modelo
        'views/occupational_group_view.xml',
        'views/cargo_viatico_view.xml',
        'views/custom_recuitment_menu.xml',
        'views/custom_recuitment_view.xml',
        'wizard/wizard_view.xml',
        #'wizard/staff_action_report.xml',
        'report/check_list_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
