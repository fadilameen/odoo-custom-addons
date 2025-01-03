from email.policy import default

from dateutil.utils import today

from odoo import fields, models
from odoo import api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    age = fields.Integer(string="Age", compute="_calculate_age")
    date_of_birth = fields.Date(string='Date of Birth', )
    gender = fields.Selection(
        string="Gender",
        selection=[('male', 'Male'), ('female', 'Female'), ])
    blood_group = fields.Selection(
        string="Blood Group",
        selection=[('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('ab+', 'AB+'), ('ab-', 'AB-'), ('b-', 'B-')])

    creation_date = fields.Date(default=fields.Datetime.now)

    @api.depends('create_date', 'date_of_birth')
    def _calculate_age(self):
        for record in self:
            if record.date_of_birth:
                record.age = (record.creation_date - record.date_of_birth).days / 365
            else:
                record.age = False
