# -*- coding: utf-8 -*-
from ast import literal_eval

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """Extension of 'res.config.settings' for configuring website bom in cart settings."""

    _inherit = "res.config.settings"

    enable_bom_in_cart = fields.Boolean(
        string='Enable Bill of Material in Cart')
    bom_product_ids = fields.Many2many('product.product',
                                       string='Choose Products',
                                       domain=[('bom_ids', '!=', False)])

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].set_param(
            'bom_in_cart.enable_bom_in_cart', self.enable_bom_in_cart)
        self.env['ir.config_parameter'].sudo().set_param(
            'bom_in_cart.bom_product_ids', self.bom_product_ids.ids)

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        bom_product_ids = params.get_param('bom_in_cart.bom_product_ids')
        res.update(enable_bom_in_cart=params.get_param(
            'bom_in_cart.enable_bom_in_cart'),
            bom_product_ids=[fields.Command.set(literal_eval(
                bom_product_ids))] if bom_product_ids else False)
        return res
