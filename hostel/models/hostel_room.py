# -*- coding: utf-8 -*-
from re import search

from dateutil.utils import today

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


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
        ('unique_tag', 'unique(room_number)', 'Same Room Already Exists'),
    ]
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
    total_rent = fields.Monetary(compute="_compute_total_rent")
    pending_amount = fields.Monetary(compute="compute_pending_amount")
    cleaning_ids = fields.One2many('cleaning.service', "room_id")

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
            # if record.student_ids:
            #     record.write({'person_count': len(record.student_ids)})
            # record.person_count = len(record.student_ids)
            record.person_count = len(
                record.student_ids) if record.student_ids else 0
            # else:
            #     record.person_count = 0

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

    def name(self, a, b=False):
        print("hello world", self)
        return [a, b]

    # def action_monthly_invoice(self):
    #
    #     print(self.room_number, (self.id), (self), self.name(10, 20))
    #     print(self.env["hostel.room"].name(5, 2))
    #     print(self.company_id.currency_id)
    #     print(sum(self.search([]).mapped('rent')))
    #     # tot = 0
    #     # for rec in self.search([]):
    #     #     tot = tot + rec.rent
    #     # print(tot)
    #     print(self.search_read([("rent", '>', 100)], ["rent"]))
    #     record_ids = self.env["sale.order"].browse(2)
    #
    #     print("search",
    #           record_ids.order_line.search(
    #               [("product_uom_qty", ">", 10), ("order_id", "=", 2)]))
    #     print("filtered", record_ids.order_line.filtered(
    #         lambda x: x.product_uom_qty > 10))
    #
    def action_monthly_invoice(self):
        """for generating monthly invoice using button"""
        if self.student_ids:
            for record in self.student_ids:
                before_30_days = date_utils.subtract(today(), months=1)
                existing_invoice = self.env['account.move'].search(
                    [("partner_id", "=", record.partner_id.id),
                     ("invoice_date", ">", before_30_days),
                     ("state", "!=", "cancel")], limit=1)
                if existing_invoice:
                    raise ValidationError(
                        "Invoice already generated this month")
                else:
                    invoice_vals = {
                        'move_type': 'out_invoice',
                        'partner_id': record.partner_id.id,
                        'student_id': record.id,
                        # 'default_state': 'posted',
                        # 'amount_total': self.total_rent,
                        'invoice_line_ids': [
                            (0, None, {
                                'product_id': self.env.ref(
                                    "hostel.hostel_rent_product").id,
                                'name': 'Hostel Rent',
                                'quantity': 1,
                                'price_unit': self.total_rent,
                                # 'price_subtotal': self.total_rent,
                            }),
                        ],
                    }
                    inv = self.env['account.move'].create([invoice_vals])
                    # inv.action_post()
                    # if record.receive_mail:
                    #     template = self.env.ref(
                    #         'account.email_template_edi_invoice')
                    #     template.send_mail(inv.id, force_send=True)

        else:
            raise ValidationError("There are no students to invoice")

    def action_monthly_automatic_invoice(self):
        """for generating monthly invoice automatically"""
        rooms_with_students = self.search([("student_ids", '!=', False)])
        for room in rooms_with_students:
            for record in room.student_ids:
                before_30_days = date_utils.subtract(today(), months=1)
                existing_invoice = room.env['account.move'].search(
                    [("partner_id", "=", record.partner_id.id),
                     ("invoice_date", ">", before_30_days),
                     ("state", "!=", "cancel")], limit=1)
                if existing_invoice:
                    continue
                invoice_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': record.partner_id.id,
                    'student_id': record.id,
                    # 'default_state': 'posted',
                    # 'amount_total': self.total_rent,
                    'invoice_line_ids': [
                        (0, None, {
                            'product_id': self.env.ref(
                                "hostel.hostel_rent_product").id,
                            'name': 'Hostel Rent',
                            'quantity': 1,
                            'price_unit': room.total_rent,
                            # 'price_subtotal': self.total_rent,
                        }),
                    ],
                }
                inv = self.env['account.move'].create([invoice_vals])
                # inv.action_post()
                # if record.receive_mail:
                #     template = self.env.ref(
                #         'account.email_template_edi_invoice')
                #     template.send_mail(inv.id, force_send=True)

    @api.depends('student_ids')
    def compute_pending_amount(self):
        """to compute pending amount in each room"""
        if self.student_ids:
            to_pay = 0
            for student in self.student_ids:
                # not_paid = student.invoice_ids.search(
                #     [("state", "=", "posted"),
                #      ("payment_state", "in", ("not_paid", "partial"))])
                not_paid = student.invoice_ids.filtered(
                    lambda inv: inv.state == "posted" and inv.payment_state in (
                        "not_paid", "partial"))
                # print(self.student_ids.invoice_ids)
                print(not_paid)
                # to_pay = sum(not_paid.mapped('amount_residual'))
                for record in not_paid:
                    to_pay += record.amount_residual
            self.pending_amount = to_pay

        else:
            self.pending_amount = 0
