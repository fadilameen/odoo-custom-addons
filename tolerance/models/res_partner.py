from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    tolerance = fields.Float(string="Tolerance", )
