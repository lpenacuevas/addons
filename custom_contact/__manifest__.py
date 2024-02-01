# -*- coding: utf-8 -*-
{
    'name': "contact customized",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Añadiendole atributos extras al modelo res_partner 
        para la institucion mitur
    """,

    'author': "Ministerio de turismo",
    'website': "https://www.mitur.gob.do",

    'category': 'Mitur/Custom_contact',
    'version': '0.1.2',
    'depends': ['base', 'mail', 'contacts','hr_recruitment','hr'],
    'application': False,
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/custom_employee.xml',
        # 'data/data_jce.xml',
        'views/custom_menu_contact.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
