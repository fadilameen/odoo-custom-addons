from odoo import models
from odoo import fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('unique_tag', 'unique(name)', ' Property type must be unique'),
    ]
