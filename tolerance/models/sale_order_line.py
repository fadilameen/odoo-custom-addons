from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tolerance = fields.Char(default=9999)
