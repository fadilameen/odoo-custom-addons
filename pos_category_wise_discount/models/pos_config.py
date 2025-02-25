# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    """Extension of 'pos.config' for configuring pos category wise discount."""
    _inherit = 'pos.config'

    is_category_wise_discount_in_pos = fields.Boolean()
    pos_category_id = fields.Many2one('pos.category')
    discount_limit = fields.Float()
