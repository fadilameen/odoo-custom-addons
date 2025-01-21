# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tolerance = fields.Float(compute="_compute_tolerance", store=True,
                             readonly=False)

    # min_qty = fields.Integer(compute="_compute_limit", store=True)
    # max_qty = fields.Integer(compute="_compute_limit", store=True)

    @api.depends("order_id")
    def _compute_tolerance(self):
        for line in self:
            line.tolerance = line.order_id.partner_id.tolerance

    # @api.onchange("tolerance", "product_uom_qty")
    # def _compute_limit(self):
    #     for line in self:
    #         qty = line.product_uom_qty
    #         line.min_qty = int(qty - (qty * line.tolerance))
    #         line.max_qty = int(qty + (qty * line.tolerance))
    #         print("qty", qty)
    #         print("min", line.min_qty, line)
    #         print("min", line.max_qty)
