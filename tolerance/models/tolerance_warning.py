# -*- coding: utf-8 -*-
from odoo import models, fields


class ToleranceWarning(models.TransientModel):
    _name = "tolerance.warning"
    _description = "Tolerance Warning"

    def action_accept(self):
        stock_picking = self.env["stock.picking"].browse(
            self._context['operation_id'])
        return stock_picking.with_context(
            skip_tolerance_check=True).button_validate()

    def action_decline(self):
        print(self._context)
        # self.action_cancel()


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_test(self):
        print("hi")
        # def action_tolerance_warning(self):
        return {'type': 'ir.actions.act_window',
                'name': 'Quantity Warning',
                'res_model': 'tolerance.warning',
                'view_mode': 'form',
                'target': 'new',

                }
