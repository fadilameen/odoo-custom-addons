# -*- coding: utf-8 -*-
import datetime
from email.policy import default

from dateutil.utils import today

from odoo import fields, api
from odoo import models


class LeaveRequest(models.Model):
    _name = "leave.request"
    _description = "Leave Request"
    _rec_name = "student_name"

    student_name = fields.Many2one("hostel.student", ondelete='cascade')
    leave_date = fields.Date(string="Leave Date", required=True)
    arrival_date = fields.Date(string="Arrival Date", required=True)
    status = fields.Selection(
        selection=[('new', 'New'), ('approved', 'Approved')], default='new')
    leave_state = fields.Selection(
        selection=[('absent', 'Absent'), ('present', 'Present')],
        compute="compute_leave_state",
    )
    current_date = fields.Date(compute="_compute_current_date")

    @api.depends('current_date', 'status')
    def compute_leave_state(self):
        """for computing the current presence of student in room"""
        for record in self:
            if record.leave_date and record.arrival_date:
                record.leave_state = 'absent' if record.leave_date <= record.current_date <= record.arrival_date and record.status == 'approved' else 'present'
            else:
                record.leave_state = 'present'

    def to_cleaning_state(self):
        """to approve the leave request"""
        self.student_name.room_id.state = 'cleaning'
        self.env["cleaning.service"].create(
            [{'room_id': self.student_name.room_id.id, }])

    def action_approve(self):
        """approve action and checking cleaning state"""
        self.status = 'approved'
        if len(self.student_name.room_id.student_ids) == len(
                self.student_name.room_id.student_ids.leave_request_ids.mapped(
                    'student_name')):
            if self.student_name.room_id.student_ids.leave_request_ids.filtered(
                    lambda lv: lv.leave_state != 'absent'):
                print("room not free")
            else:
                self.to_cleaning_state()
                print("room free")

        else:
            print("room not free")

    @api.depends("current_date")
    def _compute_current_date(self):
        self.current_date = datetime.date.today()
