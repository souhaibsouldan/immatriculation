# -*- coding: utf-8 -*-
{
    'name': "immatriculation",

    'summary': "Module de gestion des immatriculations fiscales",

    'description': """
Long description of module's purpose
    """,

    'author': "Horna Africa Technology",
    'website': "https://www.hatech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Immatriculation',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/immatriculation.xml',
        'views/menu_general.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'images': ['immatriculation,static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}

