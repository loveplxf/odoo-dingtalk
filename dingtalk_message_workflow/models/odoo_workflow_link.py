# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, SUPERUSER_ID, exceptions
from datetime import datetime

_logger = logging.getLogger(__name__)

NOTICE_MESSAGE_TEMP = """
# {
#     "msgtype": "oa",
#     "oa": {
#         "message_url": self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
#         "head": {
#             "bgcolor": "FFBBBBBB",
#             "text": "测试消息"
#         },
#         "body": {
#             "title": "我是一条测试消息-"+message,
#             "form": [
#                 {
#                     "key": "测试Key：",
#                     "value": "内容值A"
#                 }, {
#                     "key": "测试Key：",
#                     "value": "内容值B"
#                 }
#             ],
#             "content": "点击查看详细内容"
#         },
#     }
# }

"""


class OdooWorkflowLink(models.Model):
    _inherit = 'odoo.workflow.link'

    notice_user_ids = fields.Many2many('res.users', 'link_users_rel', 'button_id', 'users_id', string='用户列表')
    notice_message_template = fields.Text(string='消息模板', default=NOTICE_MESSAGE_TEMP)

    def trigger_link(self, btn_name):
        result = super().trigger_link(btn_name)
        _logger.info('--------trigger_link------------')
        return result
