# -*- coding: utf-8 -*-

import base64
import logging
import threading
import requests
from odoo import api, fields, models, exceptions, SUPERUSER_ID

UPDATEDINGTALKAVATARSTATE = False    # 替换头像的全局开关，防止重入
_logger = logging.getLogger(__name__)


class UpdateDingtalkEmployeeAvatar(models.TransientModel):
    _name = 'update.dingtalk.employee.avatar'
    _description = "替换员工头像"

    company_ids = fields.Many2many('res.company', 'dingtalk_update_employee_avatar_rel', string="同步的公司",
                                   required=True, default=lambda self: [(6, 0, [self.env.company.id])])

    def on_update(self):
        """
        确认替换头像
        :return:
        """
        self.ensure_one()
        global UPDATEDINGTALKAVATARSTATE
        if UPDATEDINGTALKAVATARSTATE:
            raise exceptions.ValidationError('系统正在后台替换所有员工的头像信息，请勿再次发起替换！')
        UPDATEDINGTALKAVATARSTATE = True  # 变为正在同步

        for company_id in self.company_ids.ids:
            company = self.env['res.company'].with_user(SUPERUSER_ID).search([('id', '=', company_id)], limit=1)
            domain = [('company_id', '=', company.id), ('ding_avatar_url', '!=', False)]
            employees = self.env['hr.employee'].sudo().search(domain)
            employees_len = len(employees)
            number = 1
            for employee in employees:
                _logger.info("%s >替换头像进度：%s / %s" % (company.name, number, employees_len))
                try:
                    binary_data = base64.b64encode(requests.get(employee.ding_avatar_url).content)
                    employee.write({'image_1920': binary_data, 'image_128': binary_data})
                    number += 1
                except Exception:
                    number += 1
                    continue
        # 完成后通知用户并修改全局设置
        UPDATEDINGTALKAVATARSTATE = False
        return {
            "name": '员工',
            "type": 'ir.actions.act_window',
            "res_model": 'hr.employee',
            "view_mode": 'kanban,tree,form,activity',
            "target": 'current'
        }