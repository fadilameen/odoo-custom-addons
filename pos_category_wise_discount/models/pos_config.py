# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_category_wise_discount_in_pos = fields.Boolean(
        string='Enable category wise discount')
    pos_category_id = fields.Many2one('pos.category',
                                      string='Select Category')
    discount_limit = fields.Float()
