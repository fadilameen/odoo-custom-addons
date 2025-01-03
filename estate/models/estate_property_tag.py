from odoo import fields
from odoo import models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_tag', 'unique(name)', ' Tag name must be unique'),
    ]
