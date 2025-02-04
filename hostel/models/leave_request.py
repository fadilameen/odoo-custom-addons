# -*- coding: utf-8 -*-
"""leave request"""
import datetime

from odoo import fields, api
from odoo import models
from odoo.tools import date_utils


class LeaveRequest(models.Model):
    """defining structure of leave requests of student"""
    _name = "leave.request"
    _description = "Leave Request"
    _rec_name = "student_id"

    student_id = fields.Many2one("hostel.student", ondelete='cascade')
    leave_date = fields.Date(string="Leave Date", required=True)
    arrival_date = fields.Date(string="Arrival Date", required=True)
    status = fields.Selection(copy=False,
                              selection=[('new', 'New'),
                                         ('approved', 'Approved')],
                              default='new')
    leave_state = fields.Selection(
        selection=[('absent', 'Absent'), ('present', 'Present')],
        compute="compute_leave_state", copy=False
    )
    current_date = fields.Date(compute="_compute_current_date")
    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.company.id)
    duration = fields.Integer(default=0, compute='_compute_duration',
                              store=True)

    @api.depends("current_date")
    def _compute_current_date(self):
        """to compute current date"""
        self.current_date = datetime.date.today()

    @api.depends('leave_date', 'arrival_date')
    def _compute_duration(self):
        """to compute duration of leave"""
        for leave in self:
            leave.duration = (
                    leave.arrival_date - leave.leave_date).days if leave.leave_date and leave.arrival_date else 0

    @api.depends('current_date', 'status')
    def compute_leave_state(self):
        """for computing the current presence of student in room"""
        for record in self:
            if record.leave_date <= record.current_date <= record.arrival_date and record.status == 'approved':
                record.leave_state = 'absent'
            else:
                record.leave_state = 'present'

    def to_cleaning_state(self):
        """to approve the leave request"""
        self.student_id.room_id.state = 'cleaning'
        self.env["cleaning.service"].create(
            [{'room_id': self.student_id.room_id.id,
              'start_time': date_utils.add(datetime.datetime.now(), hours=1)
              }])

    def action_approve(self):
        """approve action and checking cleaning state"""
        self.status = 'approved'
        if len(self.student_id.room_id.student_ids) == len(
                self.student_id.room_id.student_ids.leave_request_ids.mapped(
                    'student_id')):
            if not self.student_id.room_id.student_ids.leave_request_ids.filtered(
                    lambda lv: lv.leave_state != 'absent'):
                self.to_cleaning_state()
