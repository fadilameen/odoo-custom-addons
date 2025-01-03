from email.policy import default

from odoo import models, api
from odoo import fields
from odoo.addons.test_new_api.models.test_new_api import Related


class OpTicket(models.Model):
    _name = "op.ticket"
    _description = "OP Ticket"

    reference = fields.Char(string="Reference", readonly=True)
    patient_name = fields.Many2one("res.partner", string="Patient Name",
                                   required=True)
    serial_no = fields.Char()
    gender = fields.Selection(related="patient_name.gender")
    age = fields.Integer(related="patient_name.age")
    blood_group = fields.Selection(related="patient_name.blood_group")
    doctor_name = fields.Many2one("hr.employee", string="Doctor Name")
    currency_id = fields.Many2one('res.currency', string="Currency", )
    fee = fields.Monetary(related="doctor_name.hourly_cost")
    date_and_time = fields.Datetime(default=fields.Datetime.now())
    token_no = fields.Integer()

    @api.model
    def create(self, vals_list):
        vals_list['reference'] = self.env['ir.sequence'].next_by_code(
            'op.ticket')
        return super().create(vals_list)
