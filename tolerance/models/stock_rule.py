# -*- coding: utf-8 -*-

from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(self, product_id, product_qty, product_uom,
                               location_dest_id, name, origin, company_id,
                               values):
        vals = super()._get_stock_move_values(product_id,
                                              product_qty,
                                              product_uom,
                                              location_dest_id,
                                              name, origin,
                                              company_id,
                                              values)
        print(vals)
        print(vals.get('sale_line_id'))
        sale_line_id = vals.get('sale_line_id')
        print(sale_line_id)
        x = self.env['sale.order.line'].browse(sale_line_id)
        vals['tolerance'] = x.tolerance

        return vals
