# -*- coding: utf-8 -*-
from odoo import fields, models


class FlatFlat(models.Model):
    _name = "flat.flat"
    _description = "Flat"

    name = fields.Char(required=True)
    description = fields.Text()
    amount = fields.Float(required=True)
    flat_management_id = fields.Many2one("flat.management")
