# -*- coding: utf-8 -*-
"""hostel student"""

from dateutil.utils import today

from odoo import api, fields, models, _, Command
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class HostelStudent(models.Model):
    """Defining structure of students"""
    _name = "hostel.student"
    _description = "Hostel Student"

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
    company_id = fields.Many2one('res.company', copy=False, store=True,
                                 string="Company",
                                 default=lambda
                                     self: self.env.company.id)
    invoice_count = fields.Integer(string="Invoices", default=0,
                                   compute='_compute_invoice_count')
    invoice_ids = fields.One2many("account.move", "student_id")
    active = fields.Boolean(default=True)
    monthly_amount = fields.Monetary(string="Monthly Amount",
                                     related="room_id.total_rent")
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda
                                      self: self.env.user.company_id.currency_id,
                                  readonly=False)
    leave_request_ids = fields.One2many("leave.request",
                                        inverse_name="student_id")
    invoice_status = fields.Selection(
        selection=[('pending', 'Pending'), ('done', 'Done')],
        compute="compute_invoice_status", store=True)
    user_id = fields.Many2one("res.users", readonly=True, string="Related User")
    pending_amount = fields.Monetary(compute='_compute_pending_amount',
                                     store=True)

    @api.depends('invoice_ids.amount_residual')
    def _compute_pending_amount(self):
        """to compute pending amount"""
        for record in self:
            record.pending_amount = sum(record.invoice_ids.filtered(
                lambda inv: inv.state == "posted" and inv.payment_state in (
                    "not_paid", "partial")).mapped('amount_residual'))

    """sql constraint for unique name"""
    _sql_constraints = [
        ('unique_tag', 'unique(name)', ' Student Already Exists'),
    ]

    @api.depends("invoice_ids", "invoice_ids.state")
    def compute_invoice_status(self):
        """to compute the status of invoice """
        before_30_days = date_utils.subtract(today(), months=1)
        for record in self:
            invoice = record.invoice_ids.search(
                [("invoice_date", ">", before_30_days),
                 ("partner_id", "=", record.partner_id.id)
                 ], limit=1)
            if invoice:
                record.invoice_status = 'done'
            else:
                record.invoice_status = 'pending'

    @api.depends("invoice_ids")
    def _compute_invoice_count(self):
        """to compute the count of invoice related to a student"""
        for record in self:
            record.invoice_count = len(record.sudo().invoice_ids)

    @api.onchange('date_of_birth')
    def _onchange_date_of_birth(self):
        """for calculating age"""
        for record in self:
            if record.date_of_birth:
                record.age = (today() - record.date_of_birth).days / 365
            else:
                record.age = False

    @api.constrains('room_id')
    def _check_room_id(self):
        """restricting student allocation to room which is already full"""
        for record in self:
            if record.room_id.person_count > record.room_id.bed_count:
                raise ValidationError("No vacant rooms left")

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

    def create_student_user(self):
        """to create a user """
        user = self.env['res.users'].create([{
            'name': self.partner_id.name,
            'login': self.partner_id.email,
            'partner_id': self.partner_id.id,
            'groups_id': [
                Command.link(self.env.ref("base.group_user").id),
                Command.link(self.env.ref("hostel.hostel_student").id)]}])
        self.user_id = user.id

    def action_alot_room(self):
        """for allotting the student into available rooms"""
        room_list = self.env['hostel.room'].search(
            [("state", "not in", ["full", "cleaning"])], limit=1)
        if room_list.id:
            self.room_id = room_list.id
        else:
            raise ValidationError("No vacant rooms left")

    def action_vacate_room(self):
        """for removing the student from  rooms"""
        room_temp = self.room_id
        self.room_id = ''
        if len(room_temp.student_ids) == 0:
            room_temp.state = 'cleaning'
            self.env["cleaning.service"].create(
                [{'room_id': room_temp.id, }])
        self.active = False

    def action_get_invoice(self):
        """to display a list of invoice related to a student"""
        return {"type": "ir.actions.act_window",
                "name": "Invoices",
                "res_model": "account.move",
                'domain': [('student_id', '=', self.name)],
                "view_mode": "list,form", }

    def action_dummy(self):
        """to remove smart button's action """
        pass
