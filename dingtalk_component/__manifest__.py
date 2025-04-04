# -*- coding: utf-8 -*-
{
    'name': "钉钉客户端组件",

    'summary': """
        钉钉客户端组件""",

    'description': """
        钉钉客户端组件
        用于调用钉钉客户端组件，包括：扫码、拍照等
    """,

    'author': "Hubin",
    'website': "http://www.faway.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '阿里钉钉/组件',
    'version': '0.1',
    # any module necessary for this one to work correctly

    # always loaded
    'data': [
    ],
    'application': True,
    'assets': {
        'web.assets_backend': [
            'dingtalk_component/static/src/dingtalk.open.js',
            'dingtalk_component/static/src/dingtalk_barcode/*',
        ],
     },
    'sequence': 1,
}