# -*- coding: utf-8 -*-


from odoo import fields
from odoo import models


class HostelFacilities(models.Model):
    """Defining hostel facilities"""
    _name = "hostel.facilities"
    _description = "Facilities"

    name = fields.Char(required=True)
    charge = fields.Monetary(string="Charge")
    currency_id = fields.Many2one("res.currency", default=lambda
        self: self.env.user.company_id.currency_id)
    _sql_constraints = [
        ('price_check', 'CHECK(charge > 0)', ' Invalid Charge'),
    ]
