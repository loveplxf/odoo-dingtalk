# -*- coding: utf-8 -*-

import logging
import threading
from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, exceptions
from odoo.addons.dingtalk_base.tools import dingtalk_tool as dt
_logger = logging.getLogger(__name__)


class SynchronousDepartment(models.TransientModel):
    _name = 'dingtalk.synchronous.department'
    _description = '部门同步'

    RepeatType = [('name', '以名称判断'), ('id', '以钉钉ID')]

    company_ids = fields.Many2many('res.company', 'dingtalk_synchronous_department_rel', string="同步的公司",
                                   required=True, default=lambda self: [(6, 0, [self.env.company.id])])
    repeat_type = fields.Selection(string=u'主键判断', selection=RepeatType, default='id')

    def on_synchronous(self):
        """
        同步部门信息
        :return:
        """
        self.ensure_one()
        
        for company_id in self.company_ids.ids:
            company = self.env['res.company'].with_user(SUPERUSER_ID).search([('id', '=', company_id)], limit=1)
            try:
                client = dt.get_client(self, dt.get_dingtalk_config(self, company))
                result = client.department.list(fetch_child=True)
            except Exception as e:
                raise exceptions.ValidationError("同步部门时发生异常，原因为：{}".format(str(e)))
            number = 1
            for res in result:
                _logger.info("正在处理第%s条数据，-> %s" % (number, res))
                data = {
                    'company_id': company.id,
                    'name': res.get('name'),
                    'ding_id': res.get('id'),
                }
                if self.repeat_type == 'name':
                    domain = [('name', '=', res.get('name')), ('company_id', '=', company.id)]
                else:
                    domain = [('ding_id', '=', res.get('id')), ('company_id', '=', company.id)]
                h_department = self.env['hr.department'].search(domain)
                if h_department:
                    h_department.write(data)
                else:
                    self.env['hr.department'].create(data)
                number += 1
            number = 1
            for res in result:
                _logger.info("正在设置父部门第%s条数据，-> %s" % (number, res))
                data = {
                    'company_id': company.id,
                    'name': res.get('name'),
                    'ding_id': res.get('id'),
                }
                # 设置父部门
                if res.get('parentid') != 1:
                    domain = [('ding_id', '=', res.get('parentid')), ('company_id', '=', company.id)]
                    partner_department = self.env['hr.department'].search(domain, limit=1)
                    if partner_department:
                        data.update({'parent_id': partner_department.id})
                else:
                    data['is_root'] = True

                if self.repeat_type == 'name':
                    domain = [('name', '=', res.get('name')), ('company_id', '=', company.id)]
                else:
                    domain = [('ding_id', '=', res.get('id')), ('company_id', '=', company.id)]
                h_department = self.env['hr.department'].search(domain)
                if h_department:
                    h_department.write(data)
                else:
                    self.env['hr.department'].create(data)
                number += 1
        return {
            "name": '部门',
            "type": 'ir.actions.act_window',
            "res_model": 'hr.department',
            "view_mode": 'kanban,tree,form',
            "target": 'current'
        }
