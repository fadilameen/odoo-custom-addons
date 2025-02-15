# -*- coding: utf-8 -*-
from odoo import fields, models


class FlatManagement(models.Model):
    _name = "flat.management"
    _description = "Flat Management"

    name = fields.Char(required=True)
    flat_ids = fields.One2many("flat.flat", inverse_name="flat_management_id")
