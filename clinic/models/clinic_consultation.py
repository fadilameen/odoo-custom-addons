from email.policy import default

from odoo import models
from odoo import fields


class ClinicConsultation(models.Model):
    _name = "clinic.consultation"
    _description = "Clinic Consultation"
    serial_no = fields.Integer()
    Op_ticket_number = fields.Many2one("op.ticket")
    patient_name = fields.Many2one("res.partner", string="Patient Name", required=True)
    doctor_name = fields.Many2one("hr.employee", string="Doctor Name")
    gender = fields.Selection(related="patient_name.gender")
    age = fields.Integer(related="patient_name.age")
    date_and_time = fields.Datetime(default=fields.Datetime.now())
    weight = fields.Float()
    SpO2 = fields.Integer(string="SpO2")
    temperature = fields.Float()
    prescription = fields.One2many("clinic.prescription", "consultation_no")
