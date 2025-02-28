# -*- coding: utf-8 -*-

from odoo import models, fields


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("paytrail", "Paytrail")],
        ondelete={"paytrail": "set default"}
    )
    paytrail_merchant_id = fields.Char(string="Merchant Id")
    paytrail_secret_key = fields.Char(string="Secret Key")
