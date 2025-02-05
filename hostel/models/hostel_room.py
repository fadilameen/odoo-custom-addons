# -*- coding: utf-8 -*-
"""hostel room"""

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.fields import Datetime, Command


class HostelRoom(models.Model):
    """Defining structure of hostel rooms"""
    _name = "hostel.room"
    _description = "Hostel Room"
    _inherit = "mail.thread"
    _rec_name = "room_number"

    room_number = fields.Char(copy=False, index=True,
                              default=lambda self: _('New'),
                              readonly=True, tracking=True)
    _sql_constraints = [
        ('unique_tag', 'unique(room_number)', 'Same Room Already Exists')]
    room_type = fields.Selection(selection=[('ac', 'AC'),
                                            ('non_ac', 'Non AC')],
                                 tracking=True, default='non_ac', required=True)
    bed_count = fields.Integer(required=True, tracking=True)
    bed_count_string = fields.Char(compute="_compute_bed_count_string",
                                   store=True)
    rent = fields.Monetary(tracking=True, default=100)
    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  readonly=False)
    state = fields.Selection(selection=[('empty', 'Empty'),
                                        ('partial', 'Partial'),
                                        ('full', 'Full'),
                                        ('cleaning', 'Cleaning')],
                             compute='compute_current_state', store=True)
    student_ids = fields.One2many("hostel.student",
                                  "room_id", tracking=True)
    person_count = fields.Integer(compute='_compute_person_count', )
    facility_ids = fields.Many2many("hostel.facility", string="Facilities")
    total_rent = fields.Monetary(compute="_compute_total_rent", store=True)
    pending_amount = fields.Monetary(compute="compute_pending_amount")
    cleaning_ids = fields.One2many('cleaning.service', "room_id")

    @api.depends('student_ids')
    def compute_pending_amount(self):
        """to compute pending amount in each room"""
        self.pending_amount = sum(self.student_ids.invoice_ids.filtered(
            lambda inv: inv.state == "posted" and inv.payment_state in (
                "not_paid", "partial")).mapped(
            'amount_residual')) if self.student_ids else 0

    @api.depends('rent', 'facility_ids')
    def _compute_total_rent(self):
        """for calculating total rent"""
        self.total_rent = sum(self.facility_ids.mapped('charge')) + self.rent

    @api.depends('bed_count')
    def _compute_bed_count_string(self):
        """for converting the bed count into string"""
        for record in self:
            record.bed_count_string = str(
                record.bed_count) if record.bed_count else "0"

    @api.depends("student_ids")
    def _compute_person_count(self):
        """for getting the person counts per room"""
        for record in self:
            record.person_count = len(
                record.student_ids) if record.student_ids else 0

    @api.depends('person_count', 'bed_count', "student_ids", "cleaning_ids")
    def compute_current_state(self):
        """for changing the state of room according to count of students per room"""
        for room in self:
            if room.cleaning_ids.filtered(lambda cln: cln.state != "done"):
                self.state = 'cleaning'
                continue
            if room.bed_count == 0:
                self.state = 'full'
            elif room.person_count == 0:
                self.state = 'empty'
            elif room.person_count >= room.bed_count:
                self.state = 'full'
            else:
                self.state = 'partial'

    @api.model_create_multi
    def create(self, vals):
        """for generating sequence number for room"""
        for val in vals:
            val['room_number'] = self.env["ir.sequence"].next_by_code(
                'room_sequence_code')
        return super(HostelRoom, self).create(vals)

    def _create_invoice(self, rent):
        """to create invoice"""
        current_date = Datetime.today()
        first_day_of_month = current_date.replace(day=1)
        invoices_created = []
        for student in self.student_ids:
            existing_invoice = self.env['account.move'].search([
                ("partner_id", "=", student.partner_id.id),
                ("invoice_date", ">=", first_day_of_month),
                ("state", "!=", "cancel")
            ], limit=1)
            if existing_invoice:
                continue
            inv = self.env['account.move'].create([{
                'move_type': 'out_invoice',
                'partner_id': student.partner_id.id,
                'student_id': student.id,
                'invoice_line_ids': [
                    Command.create({
                        'product_id': self.env.ref(
                            "hostel.hostel_rent_product").id,
                        'name': 'Hostel Rent',
                        'quantity': 1,
                        'price_unit': rent,
                    })],
            }])
            if inv:
                invoices_created.append(inv)
        return invoices_created

    def action_monthly_invoice(self):
        """Generate monthly invoice using button"""
        if not self._create_invoice(self.total_rent):
            raise ValidationError("No students left to invoice this month")

    def action_monthly_automatic_invoice(self):
        """Automatically generate monthly invoices."""
        for room in self.search([("student_ids", '!=', False)]):
            room._create_invoice(room.total_rent)
