# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """Extension of 'res.config.settings' for configuring pos category wise discount."""
    _inherit = "res.config.settings"

    is_category_wise_discount_in_pos = fields.Boolean(
        string='Enable category wise discount',
        related='pos_config_id.is_category_wise_discount_in_pos',
        readonly=False)
    pos_category_id = fields.Many2one('pos.category',
                                      string='Select Category',
                                      related='pos_config_id.pos_category_id',
                                      readonly=False)
    discount_limit = fields.Float(related='pos_config_id.discount_limit',
                                  readonly=False)
