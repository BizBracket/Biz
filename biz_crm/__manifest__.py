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
        'base','crm', 'sale'],
    'data': [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/mailtemplate.xml",
        "views/crm_lead_inherit.xml",
        "views/branch_view.xml",
        "views/sale_order_view.xml"
    ],
    'installable': True,
    'auto_install': False,
}
