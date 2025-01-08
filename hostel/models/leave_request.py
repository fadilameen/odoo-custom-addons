# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models


class LeaveRequest(models.Model):
    _name = "leave.request"
    _description = "Leave Request"
    _rec_name = "student_name"

    student_name = fields.Many2one("hostel.student", ondelete='cascade')
    leave_date = fields.Date(string="Leave Date")
    arrival_date = fields.Date(string="Arrival Date")
    status = fields.Selection(
        selection=[('new', 'New'), ('approved', 'Approved')], )

    def action_approve(self):
        """to approve the leave request"""
        self.status = 'approved'
        # print(len(self.student_name.room_id.student_ids))
        if len(self.student_name.room_id.student_ids) == 1:
            self.student_name.room_id.state = 'cleaning'
            self.env["cleaning.service"].create(
                [{'room_id': self.student_name.room_id.id, }])
