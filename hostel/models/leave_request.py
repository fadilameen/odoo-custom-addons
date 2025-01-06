# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models


class LeaveRequest(models.Model):
    _name = "leave.request"
    _description = "Leave Request"
    _rec_name = "student_name"

    student_name = fields.Many2one("hostel.student")
    leave_date = fields.Date(string="Leave Date")
    arrival_date = fields.Date(string="Arrival Date")
    status = fields.Selection(
        selection=[('new', 'New'), ('approved', 'Approved')], )

    def action_approve(self):
        """to approve the leave request"""
        self.status = 'approved'
