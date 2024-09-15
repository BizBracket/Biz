# -*- coding: utf-8 -*-
{
    'name': 'biz_crm',
    'version': '1.0',
    "sequence": 1,
    'complexity': "",
    'category': 'Generic Modules/Others',
    'description': """


    """,
    'author': '',
    'website': '',
    'depends': [
        'base','crm'],
    'data': [
        "security/ir.model.access.csv",
        "data/mailtemplate.xml",
        "views/crm_lead_inherit.xml",
    ],
    'installable': True,
    'auto_install': False,
}
