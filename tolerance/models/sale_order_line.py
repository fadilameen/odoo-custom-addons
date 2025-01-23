# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tolerance = fields.Float(string="Tolerance", compute="_compute_tolerance",
                             store=True, readonly=False)

    @api.depends("order_id.partner_id")
    def _compute_tolerance(self):
        for line in self:
            line.tolerance = line.order_id.partner_id.tolerance

    # def _prepare_procurement_values(self, **kwargs):
    #     values = super()._prepare_procurement_values(
    #         **kwargs)
    #     values['tolerance'] = self.tolerance
    #     return values
