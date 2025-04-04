# -*- coding: utf-8 -*-
import base64
import logging
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.addons.dingtalk_base.tools import dingtalk_tool as dt

_logger = logging.getLogger(__name__)


class DingtalkLog(models.Model):
    _description = "消息日志"
    _name = 'dingtalk.message.log'
    _order = 'id desc'

    company_id = fields.Many2one('res.company', string='公司', default=lambda self: self.env.user.company_id)
    name = fields.Char(string="名称")
    msg_type = fields.Selection(string="消息类型", selection=[('chat', '群消息'), ('work', '工作通知'), ('msg', '普通消息')])
    to_user = fields.Char(string="发送对象")
    body = fields.Text(string="消息内容")
    result = fields.Text(string="返回结果")


class DingTalkMessage(models.TransientModel):
    _name = 'dingtalk.message'
    _description = "发送消息"

    @api.model
    def send_work_message(self, userid_list, message):
        """
        发送工作消息到指定员工列表
        :param userid_list 员工列表  string
        :param message 消息内容
        :return:
        """
        config = dt.get_dingtalk_config(self, self.env.user.company_id)
        client = dt.get_client(self, config)
        msg_body = message
        try:
            result = client.message.send(
                config.agent_id, msg_body, touser_list=userid_list, toparty_list=())
            logging.info(">>>发送工作通知消息返回结果%s", result)
            # 创建消息日志
            self.env['dingtalk.message.log'].create({
                'company_id': self.env.user.company_id.id,
                'name': "发送工作通知",
                'msg_type': "work",
                'to_user': ','.join(userid_list),
                'body': message,
                'result': result,
            })
        except Exception as e:
            raise UserError(e)
        return True

    @api.model
    def send_work_message_test(self, userid_list, message):
        """
        发送工作消息到指定员工列表
        :param userid_list 员工列表  string
        :param message 消息内容
        :return:
        """
        config = dt.get_dingtalk_config(self, self.env.user.company_id)
        client = dt.get_client(self, config)
        msg_body = {
            "msgtype": "oa",
            "oa": {
                "message_url": self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
                "head": {
                    "bgcolor": "FFBBBBBB",
                    "text": "测试消息"
                },
                "body": {
                    "title": "我是一条测试消息-"+message,
                    "form": [
                        {
                            "key": "测试Key：",
                            "value": "内容值A"
                        }, {
                            "key": "测试Key：",
                            "value": "内容值B"
                        }
                    ],
                    "content": "点击查看详细内容"
                },
            }
        }
        try:
            result = client.message.send(
                config.agent_id, msg_body, touser_list=userid_list, toparty_list=())
            logging.info(">>>发送测试消息返回结果%s", result)
        except Exception as e:
            raise UserError(e)
        return True
