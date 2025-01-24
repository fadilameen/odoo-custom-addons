# -*- coding: utf-8 -*-
from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    tolerance = fields.Float(string="Tolerance")

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            sale_line_id = val.get('sale_line_id')
            purchase_line_id = val.get('purchase_line_id')
            if sale_line_id:
                print(sale_line_id)
                tolerance = self.env["sale.order.line"].browse(
                    sale_line_id).tolerance
                print(tolerance)
                val['tolerance'] = tolerance
            if purchase_line_id:
                print(purchase_line_id)
                tolerance = self.env["purchase.order.line"].browse(
                    purchase_line_id).tolerance
                print(tolerance)
                val['tolerance'] = tolerance
        return super().create(vals)
