# -*- coding: utf-8 -*-
{
    'name': "钉钉集成-工作流消息通知",
    'summary': """用于支持Odoo工作流集成钉钉消息通知功能""",
    'description': """用于支持Odoo工作流集成钉钉消息通知功能""",
    'author': "hubin",
    'website': "https://www.faway.vip",
    'category': '阿里钉钉/工作流消息通知',
    'version': '17.1.1',
    'license': 'OPL-1',
    'depends': ['dingtalk_message', 'odoo_dynamic_workflow'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'data': [
        'views/odoo_workflow_link_view.xml'
    ]
}
