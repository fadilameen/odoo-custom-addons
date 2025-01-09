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
    partner_id = fields.Many2one("res.partner", readonly=True,
                                 string="Related Partner")
    student_id = fields.Char(string="Student ID",
                             default=lambda self: _('New'), readonly=True)
    date_of_birth = fields.Datetime(default=False)
    age = fields.Integer(string="Age")
    room_id = fields.Many2one("hostel.room", readonly=True)
    email = fields.Char(string="Email", required=True)
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

    active = fields.Boolean(default=True)
    monthly_amount = fields.Monetary(string="Monthly Amount",
                                     related="room_id.total_rent")

    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda
                                      self: self.env.user.company_id.currency_id,
                                  readonly=False,
                                  )
    invoice_status = fields.Selection(
        selection=[('pending', 'Pending'), ('done', 'Done')],
        compute="_compute_invoice_status"
    )
    user_id = fields.Many2one("res.users", readonly=True, string="Related User")

    @api.depends("invoice_ids")
    def _compute_invoice_status(self):
        invoice = self.invoice_ids.search(
            [("invoice_date", ">", "2024-12-09"),
             ("partner_id", "=", self.partner_id.id)
             ], limit=1)
        if invoice:
            self.invoice_status = 'done'
        else:
            self.invoice_status = 'pending'

        # for record in self.invoice_ids:

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
        # print(room_list.id)
        if room_list.id:
            self.room_id = room_list.id
        else:
            raise ValidationError("No vacant rooms left")

    def action_vacate_room(self):
        """for removing the student from  rooms"""
        # print(len(self.room_id.student_ids))
        room_temp = self.room_id
        self.room_id = ''
        # print(room_temp.state, "x1")
        if len(self.room_id.student_ids) == 0:
            room_temp.state = 'cleaning'
            # print(room_temp.state, "x2")
            self.env["cleaning.service"].create(
                [{'room_id': room_temp.id, }])
        self.active = False

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

    def create_student_user(self):
        user = self.env['res.users'].create([{
            'name': self.partner_id.name,
            'login': self.partner_id.email,
            'partner_id': self.partner_id.id,
        }])
        self.user_id = user.id

    # def create_student_user(self):
    #     user_vals = {
    #         'name': self.partner_id.name,
    #         'login': self.partner_id.name,
    #         'partner_id': self.partner_id.id,
    #     }
    #     user = self.env['res.users'].create(user_vals)
    #     self.user_id = user.id
