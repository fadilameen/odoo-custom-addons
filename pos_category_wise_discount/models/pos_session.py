# -*- coding: utf-8 -*-
from odoo import api, models


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_fields(self, config_id):
        print("Hello World!")
        params = self.env['ir.config_parameter'].sudo()
        is_category_wise_discount_in_pos = params.get_param(
            'pos_category_wise_discount.is_category_wise_discount_in_pos')
        pos_category_id = params.get_param(
            'pos_category_wise_discount.pos_category_id')
        discount_limit = params.get_param(
            'pos_category_wise_discount.discount_limit')
        data = super()._load_pos_data_fields(config_id)
        # data += ['age']
        print(is_category_wise_discount_in_pos, pos_category_id, discount_limit)
        print(self.env['pos.config'].search(
            [('company_id', '=', self.env.company.id)], order='write_date desc',
            limit=1).read())
        return data
