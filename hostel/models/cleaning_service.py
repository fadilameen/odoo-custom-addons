# -*- coding: utf-8 -*-
"""Cleaning Service model of hostel module"""

from odoo import fields, models


class CleaningService(models.Model):
    """defining structure of cleaning service model"""
    _name = "cleaning.service"
    _description = "Cleaning Service"
    _rec_name = "room_id"

    room_id = fields.Many2one("hostel.room", required=True, ondelete='cascade')
    start_time = fields.Datetime(string="Start Time")
    cleaning_staff = fields.Many2one("res.users")
    state = fields.Selection(
        selection=[('new', 'New'), ('assigned', 'Assigned'), ('done', 'Done')],
        default='new')
    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.company.id)

    def action_assign_cleaning_service(self):
        """assign button action to assign current user"""
        self.cleaning_staff = self.env.user
        self.state = "assigned"

    def action_complete(self):
        """Complete button action"""
        self.state = "done"
        self.room_id.compute_current_state()
