# -*- coding: utf-8 -*-
from email.policy import default
from itertools import count

from dateutil.utils import today

from odoo import api, fields, models, _
from odoo.api import readonly
from odoo.exceptions import ValidationError


class HostelStudent(models.Model):
    """Defining structure of students"""

    _name = "hostel.student"
    _description = "Hostel Student"
    # _rec_name = "name"

    name = fields.Char(string="Student Name")
    partner_id = fields.Many2one("res.partner", readonly=True)
    student_id = fields.Char(string="Student ID",
                             default=lambda self: _('New'), readonly=True)
    date_of_birth = fields.Datetime(default=False)
    age = fields.Integer(string="Age")
    room_id = fields.Many2one("hostel.room", readonly=True)
    email = fields.Char(string="Email")
    image = fields.Image(string="Image")
    receive_mail = fields.Boolean(default=False, )
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string="State",
                               domain="[('country_id', '=?', country_id)]")
    zip = fields.Char(string="Zip")
    country_id = fields.Many2one("res.country", string="Country")
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    invoice_count = fields.Integer(string="Invoices", default=0,
                                   compute='_compute_invoice_count')
    invoice_ids = fields.One2many("account.move", "student_id")

    # leave_request_ids = fields.One2many("leave.request", "student_name",
    #                                     ondelete='cascade')

    @api.depends("invoice_ids")
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    @api.constrains('room_id')
    def _check_room_id(self):
        """restricting student allocation to room which is already full"""
        for record in self:
            if record.room_id.person_count > record.room_id.bed_count:
                raise ValidationError("No vacant rooms left")

    _sql_constraints = [
        ('unique_tag', 'unique(name)', ' Student Already Exists'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """for generating sequence number for student and create partner when creating student"""

        for val in vals_list:
            val['student_id'] = self.env["ir.sequence"].next_by_code(
                "student_sequence_code")

            partner = self.env['res.partner'].create([{
                'name': val.get('name'),
                'email': val.get('email'),
                'street': val.get('street'),
                'street2': val.get('street2'),
                'city': val.get('city'),
                'state_id': val.get('state_id'),
                'zip': val.get('zip'),
                'country_id': val.get('country_id')
            }])

            val['partner_id'] = partner.id

            return super(HostelStudent, self).create(vals_list)

    def action_alot_room(self):
        """for allotting the student into available rooms"""
        room_list = self.env['hostel.room'].search(
            [('state', '!=', 'full')], limit=1)
        print(room_list.id)
        if room_list.id:
            self.room_id = room_list.id
        else:
            raise ValidationError("No vacant rooms left")

    def action_vacate_room(self):
        """for removing the student from  rooms"""
        self.room_id = ''

    @api.onchange('date_of_birth')
    def _onchange_date_of_birth(self):
        """for calculating age"""
        for record in self:
            if record.date_of_birth:
                record.age = (today() - record.date_of_birth).days / 365
            else:
                record.age = False

    def action_get_invoice(self):
        print(self.name)
        return {
            "type": "ir.actions.act_window",
            "name": "Invoices",
            "res_model": "account.move",
            'domain': [('student_id', '=', self.name)],
            "view_mode": "list,form",
        }
