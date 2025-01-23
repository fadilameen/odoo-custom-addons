from odoo import models, fields


class ToleranceWarning(models.TransientModel):
    _name = "tolerance.warning"
    _description = "Tolerance Warning"

    def action_accept(self):
        x = self.env["stock.picking"].browse(
            self._context['operation_id']).button_validate()
        print(x)

    def action_decline(self):
        print(self._context)
        self.env["stock.picking"].browse(
            self._context['operation_id']).action_cancel()
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
