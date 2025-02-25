# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    brand = fields.Char()

    def _load_pos_data_fields(self, config_id):
        """pass brand into pos"""
        data = super()._load_pos_data_fields(config_id)
        data += ['brand']
        return data
