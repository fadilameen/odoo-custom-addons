# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """Extension of 'res.config.settings' for configuring pos category wise discount."""
    _inherit = "res.config.settings"

    is_category_wise_discount_in_pos = fields.Boolean(
        string='Enable category wise discount')
    pos_category_id = fields.Many2one('pos.category',
                                      string='Select Category')
    discount_limit = fields.Float()

    def set_values(self):
        """to set values into settings"""
        super().set_values()
        self.env['ir.config_parameter'].set_param(
            'pos_category_wise_discount.is_category_wise_discount_in_pos',
            self.is_category_wise_discount_in_pos)
        self.env['ir.config_parameter'].sudo().set_param(
            'pos_category_wise_discount.pos_category_id',
            self.pos_category_id.id)
        self.env['ir.config_parameter'].sudo().set_param(
            'pos_category_wise_discount.discount_limit',
            self.discount_limit)

    @api.model
    def get_values(self):
        """to get values from settings"""
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        is_category_wise_discount_in_pos = params.get_param(
            'pos_category_wise_discount.is_category_wise_discount_in_pos')
        pos_category_id = params.get_param(
            'pos_category_wise_discount.pos_category_id')
        discount_limit = params.get_param(
            'pos_category_wise_discount.discount_limit')
        res.update(
            is_category_wise_discount_in_pos=is_category_wise_discount_in_pos,
            pos_category_id=int(pos_category_id) if pos_category_id else False,
            discount_limit=float(discount_limit))
        return res
