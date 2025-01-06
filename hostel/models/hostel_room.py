# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


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

    @api.depends('bed_count')
    def _compute_bed_count_string(self):
        for record in self:
            record.bed_count_string = str(
                record.bed_count) if record.bed_count else "0"

    rent = fields.Monetary(tracking=True)
    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  readonly=False,
                                  )
    state = fields.Selection(selection=[('empty', 'Empty'),
                                        ('partial', 'Partial'),
                                        ('full', 'Full')],
                             compute='_compute_current_state', store=True)
    student_ids = fields.One2many("hostel.student",
                                  "room_id")
    person_count = fields.Integer(compute='_compute_person_count', )

    facility_id = fields.Many2many("hostel.facility", string="Facilities")

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

    @api.depends('person_count', 'bed_count', "student_ids")
    def _compute_current_state(self):
        """for changing the state of room according to count of students per room"""
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
                print("else working")

        # for record in self:
        #     if record.student_ids:
        #         if record.person_count:
        #             if record.person_count > 0:
        #                 record.write({'state': 'partial'})
        #             if record.person_count >= record.bed_count:
        #                 record.write({'state': 'full'})
        #                 # state = 'full'
        #     # elif record.person_count == 0:
        #     #     record.write({'state': 'empty'})
        #     else:
        #         if record.bed_count != 0:
        #             record.write({'state': 'empty'})
        #             print("else working")
        #         else:
        #             record.write({'state': 'full'})

    @api.model_create_multi
    def create(self, vals):
        """for generating sequence number for room"""
        for val in vals:
            val['room_number'] = self.env["ir.sequence"].next_by_code(
                'room_sequence_code')
        return super(HostelRoom, self).create(vals)
