# -*- coding: utf-8 -*-
from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    tolerance = fields.Float(string="Tolerance")

    @api.model
    def create(self, vals):
        """
        Ensures tolerance is set from procurement or sale order line.
        """
        if not vals.get('tolerance') and 'sale_line_id' in vals:
            sale_line = self.env['sale.order.line'].browse(vals['sale_line_id'])
            vals['tolerance'] = sale_line.tolerance
        return super(StockMove, self).create(vals)
