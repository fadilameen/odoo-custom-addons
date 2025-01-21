# -*- coding: utf-8 -*-

from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    tolerance = fields.Float(compute="_compute_tolerance", store=True,
                             readonly=False)

    @api.depends("order_id")
    def _compute_tolerance(self):
        for record in self:
            record.tolerance = record.order_id.partner_id.tolerance
