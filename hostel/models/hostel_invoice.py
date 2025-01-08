# -*- coding: utf-8 -*-

from odoo import fields, api
from odoo import models
from odoo.api import ValuesType, Self


class AccountMove(models.Model):
    _inherit = "account.move"

    student_id = fields.Many2one("hostel.student", string='Student')
