# -*- coding: utf-8 -*-

from dateutil.utils import today

from odoo import _
from odoo import api
from odoo import fields
from odoo import models
from odoo.exceptions import ValidationError


class HostelStudent(models.Model):
    """Defining structure of students"""

    _name = "hostel.student"
    _description = "Hostel Student"

    name = fields.Many2one("res.partner", required=True,
                           string="Student Name")
    student_id = fields.Char(string="Student ID",
                             default=lambda self: _('New'), readonly=True)
    date_of_birth = fields.Datetime(default=False)
    age = fields.Integer(string="Age", compute="_compute_calculate_age")
    room_no = fields.Many2one("hostel.room", readonly=True)
    email = fields.Char(related="name.email")
    image = fields.Image(string="Image")
    receive_mail = fields.Boolean(default=False)
    street = fields.Char(related="name.street")
    street2 = fields.Char(related="name.street2")
    city = fields.Char(related="name.city")
    state_id = fields.Many2one(related="name.state_id")
    zip = fields.Char(related="name.zip")
    country_id = fields.Many2one(related="name.country_id")
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)

    @api.constrains('room_no')
    def _constrains_check_room(self):
        """restricting student allocation to room which is already full"""
        for record in self:
            if record.room_no.person_count > record.room_no.number_of_beds:
                raise ValidationError("No vacant rooms left")

    _sql_constraints = [
        ('unique_tag', 'unique(name)', ' Student Already Exists'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """for generating sequence number for student"""

        for val in vals_list:
            val['student_id'] = self.env["ir.sequence"].next_by_code(
                "student_sequence_code")
            return super(HostelStudent, self).create(vals_list)

    def action_alot_room(self):
        room_list = self.env['hostel.room'].search(
            [('state', '!=', 'full')], limit=1)
        print(room_list.id)
        if room_list.id:
            self.room_no = room_list.id
        else:
            raise ValidationError("No vacant rooms left")

    @api.depends('date_of_birth')
    def _compute_calculate_age(self):
        """for calculating age"""
        for record in self:
            if record.date_of_birth:
                record.age = (today() - record.date_of_birth
                              ).days / 365
            else:
                record.age = False
