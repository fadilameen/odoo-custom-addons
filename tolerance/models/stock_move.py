# -*- coding: utf-8 -*-
from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    tolerance = fields.Float(string="Tolerance")

    # @api.model_create_multi
    # def create(self, vals):
    #     for val in vals:
    #         if not val.get('tolerance') and 'sale_line_id' in val:
    #             sale_line = self.env['sale.order.line'].browse(
    #                 val['sale_line_id'])
    #             val['tolerance'] = sale_line.tolerance
    #     return super(StockMove, self).create(vals)
