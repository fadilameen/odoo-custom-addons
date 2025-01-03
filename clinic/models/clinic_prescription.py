from odoo import models
from odoo import fields


class ClinicPrescription(models.Model):
    _name = "clinic.prescription"
    _description = "Clinic Prescription"

    consultation_no = fields.Many2one("clinic.consultation")
    patient_name = fields.Many2one(string="Patient Name", related="consultation_no.patient_name")
    medicine = fields.Many2one("product.template")
    quantity = fields.Integer()
    dosage = fields.Text()
