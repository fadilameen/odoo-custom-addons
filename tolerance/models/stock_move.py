# -*- coding: utf-8 -*-
from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    tolerance = fields.Float()

    @api.onchange("tolerance")
    def test(self):
        print("fun ")
        x = (self.env["stock.picking"].search([("origin", "=", self.origin)]))
        for y in x:
            for record in (y.move_ids_without_package.product_id):
                print(record.name)

    # min_qty = fields.Integer(compute="_compute_limit", store=True)
    # max_qty = fields.Integer(compute="_compute_limit", store=True)

    # @api.depends("picking_id")
    # def _compute_tolerance(self):
    #     for line in self:
    #         line.tolerance = line.order_id.partner_id.tolerance

    # @api.onchange("tolerance", "product_uom_qty")
    # def _compute_limit(self):
    #     for line in self:
    #         qty = line.product_uom_qty
    #         line.min_qty = int(qty - (qty * line.tolerance))
    #         line.max_qty = int(qty + (qty * line.tolerance))
    #         print("qty", qty)
    #         print("min", line.min_qty, line)
    #         print("min", line.max_qty)
