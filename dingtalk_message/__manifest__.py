# -*- coding: utf-8 -*-
{
    'name': "钉钉集成-消息通知",
    'summary': """用于支持Odoo集成钉钉消息通知功能""",
    'description': """用于支持Odoo集成钉钉消息通知功能""",
    'author': "hubin",
    'website': "https://www.faway.vip",
    'category': '阿里钉钉/消息通知',
    'version': '17.1.1',
    'license': 'OPL-1',
    'depends': ['dingtalk_base'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'views/dingtalk_message.xml',
        'views/hr_employee.xml'
    ]
}
