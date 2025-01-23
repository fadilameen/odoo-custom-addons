from odoo import models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for move in self.move_ids:
            tolerance = move.product_uom_qty * move.tolerance
            min_qty = move.product_uom_qty - tolerance
            max_qty = move.product_uom_qty + tolerance
            print(min_qty, "min")
            print(max_qty, "max")
            if not (min_qty < move.quantity < max_qty):
                print("quantity scnaan machu")
                return {'type': 'ir.actions.act_window',
                        'name': 'Quantity Warning',
                        'res_model': 'tolerance.warning',
                        'view_mode': 'form',
                        'target': 'new',
                        'context': {'operation_id': self.id}
                        }

                # raise ValidationError("quantity scnaan machu")

        return super().button_validate()
