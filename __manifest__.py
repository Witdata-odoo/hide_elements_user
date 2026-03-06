# -*- coding: utf-8 -*-
{
'name': 'Hide Elements User Wise',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Hide buttons and make forms read-only per user.',
    'description': 'It allows the administrator to hide specific buttons or force read-only mode on particular models for specific users without creating complex security groups.',
    'author': 'Freancisco Sulé',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hide_rule_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
