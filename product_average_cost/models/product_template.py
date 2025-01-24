# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_average_cost = fields.Float(
        compute="_compute_product_average_cost")

    def _compute_product_average_cost(self):
        """to compute average cost of products"""
        product_product_id = self.env["product.product"].search(
            [("product_tmpl_id", "in", [self.id])])
        order_lines = self.env["purchase.order"].search(
            [("product_id", "in", product_product_id.ids),
             ("state", "=", "purchase")]).order_line.filtered(
            lambda p: p.product_id.product_tmpl_id.id == self.id)
        print(order_lines.mapped('product_uom_qty'), "yyy")
        total_amount = sum(order_lines.mapped('price_subtotal'))
        total_quantity = sum(order_lines.mapped('product_uom_qty'))
        try:
            average_cost = total_amount / total_quantity
            self.product_average_cost = average_cost
        except ZeroDivisionError:
            self.product_average_cost = 0
