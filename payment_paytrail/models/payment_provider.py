# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("paytrail", "Paytrail")],
        ondelete={"paytrail": "set default"}
    )
    paytrail_merchant_id = fields.Char(string="Merchant Id")
    paytrail_secret_key = fields.Char(string="Secret Key")

    def _prepare_paytrail_header(self):
        # print(str(uuid.uuid4()))
        # print(fields.datetime.now().isoformat())
        print(self.read())
        headers = {
            "checkout-account": self.paytrail_merchant_id,
            "checkout-algorithm": "sha256",
            "checkout-method": "POST",
            "checkout-nonce": str(uuid.uuid4()),
            "checkout-timestamp": str(fields.datetime.now().isoformat())
        }
        return headers
