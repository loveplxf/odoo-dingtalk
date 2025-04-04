# -*- coding: utf-8 -*-
from dingtalk import DingTalkClientException
from odoo import api, SUPERUSER_ID, http
from odoo.exceptions import UserError
from odoo.http import Controller, json, request
from odoo.addons.dingtalk_base.tools import dingtalk_tool as dt


def error_response(error, msg):
    res = {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 200,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }
    return http.Response(
        json.dumps(res),
        status=200,
        mimetype='application/json'
    )


def success_response(data):
    res = {
        "jsonrpc": "2.0",
        "id": None,
        "result": data
    }
    return http.Response(
        json.dumps(res),
        status=200,
        mimetype='application/json'
    )


class DingTalkAPI(Controller):

    @http.route('/web/dingtalk/get_userinfo', type='http', auth='none', website=True, sitemap=False)
    def dingtalk_get_userinfo(self, **kw):
        """
        通过获得钉钉小程序用户信息
        :param kw:
        :return:
        """
        params_data = request.params.copy()
        try:
            corp_id = params_data["corp_id"]
        except KeyError as e:
            return error_response(e, 'corp_id作为参数必须输入')

        try:
            auth_code = params_data["auth_code"]
        except KeyError as e:
            return error_response(e, 'auth_code作为参数必须输入')

        try:
            config = request.env['dingtalk.config'].with_user(SUPERUSER_ID).search([('corp_id', '=', corp_id)], limit=1)
            client = dt.get_client(request, dt.get_dingtalk_config(request, config.company_id))
        except UserError as e:
            return error_response(e, '获取钉钉参数失败')

        try:
            userinfo = client.user.getuserinfo(auth_code)
        except DingTalkClientException as e:
            return error_response(e, '钉钉获取用户信息失败')

        return success_response(userinfo)
