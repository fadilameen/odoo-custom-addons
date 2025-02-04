# -*- coding: utf-8 -*-
"""hostel room"""

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.fields import Datetime


class HostelRoom(models.Model):
    """Defining structure of hostel rooms"""
    _name = "hostel.room"
    _description = "Hostel Room"
    _inherit = "mail.thread"
    _rec_name = "room_number"

    room_number = fields.Char(copy=False, index=True,
                              default=lambda self: _('New'),
                              readonly=True, string="Room Number")
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
                                  readonly=False,
                                  )
    state = fields.Selection(selection=[('empty', 'Empty'),
                                        ('partial', 'Partial'),
                                        ('full', 'Full'),
                                        ('cleaning', 'Cleaning')],
                             compute='compute_current_state', store=True)
    student_ids = fields.One2many("hostel.student",
                                  "room_id")
    person_count = fields.Integer(compute='_compute_person_count', )

    facility_id = fields.Many2many("hostel.facility", string="Facilities")
    total_rent = fields.Monetary(compute="_compute_total_rent", store=True)
    pending_amount = fields.Monetary(compute="compute_pending_amount")
    cleaning_ids = fields.One2many('cleaning.service', "room_id")

    @api.depends('student_ids')
    def compute_pending_amount(self):
        """to compute pending amount in each room"""
        if self.student_ids:
            to_pay = 0
            for student in self.student_ids:
                not_paid = student.invoice_ids.filtered(
                    lambda inv: inv.state == "posted" and inv.payment_state in (
                        "not_paid", "partial"))
                for record in not_paid:
                    to_pay += record.amount_residual
            self.pending_amount = to_pay
        else:
            self.pending_amount = 0

    @api.depends('rent', 'facility_id')
    def _compute_total_rent(self):
        """for calculating total rent"""
        for record in self:
            facilities_total = 0
            for facility in record.facility_id:
                facilities_total += facility.charge
            record.total_rent = record.rent + facilities_total

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
        cln = self.cleaning_ids.filtered(lambda cln: cln.state != "done")
        for record in self:
            if record.bed_count == 0:
                record.write({'state': 'full'})
            elif record.person_count:
                if record.person_count >= record.bed_count:
                    record.write({'state': 'full'})
                else:
                    record.write({'state': 'partial'})
            else:
                record.write({'state': 'empty'})
        if cln:
            self.state = 'cleaning'

    @api.model_create_multi
    def create(self, vals):
        """for generating sequence number for room"""
        for val in vals:
            val['room_number'] = self.env["ir.sequence"].next_by_code(
                'room_sequence_code')
        return super(HostelRoom, self).create(vals)

    def _create_invoice(self, student, rent):
        """to create invoice"""
        current_date = Datetime.today()
        first_day_of_month = current_date.replace(day=1)
        existing_invoice = self.env['account.move'].search([
            ("partner_id", "=", student.partner_id.id),
            ("invoice_date", ">", first_day_of_month),
            ("state", "!=", "cancel")
        ], limit=1)
        print(student.partner_id.id)
        if existing_invoice:
            return

        inv = self.env['account.move'].create([{
            'move_type': 'out_invoice',
            'partner_id': student.partner_id.id,
            'student_id': student.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.env.ref("hostel.hostel_rent_product").id,
                'name': 'Hostel Rent',
                'quantity': 1,
                'price_unit': rent,
            })],
        }])
        return inv

    def action_monthly_invoice(self):
        """Generate monthly invoice using button"""
        invoices_created = []
        if not self.student_ids:
            raise ValidationError("No students to invoice")
        for student in self.student_ids:
            inv = (self._create_invoice(student, self.total_rent))
            print(inv)
            if inv:
                invoices_created.append(inv)
        if not invoices_created:
            raise ValidationError("No students left to invoice this month")

    def action_monthly_automatic_invoice(self):
        print(self)
        """Automatically generate monthly invoices."""
        for room in self.search([("student_ids", '!=', False)]):
            for student in room.student_ids:
                (self._create_invoice(student, room.total_rent))
