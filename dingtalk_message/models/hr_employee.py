# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, SUPERUSER_ID, exceptions
from datetime import datetime

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def send_work_message_test(self):
        self.ensure_one()
        self.env['dingtalk.message'].send_work_message_test([self.ding_id], str(datetime.now().second))
