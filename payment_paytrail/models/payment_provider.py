# -*- coding: utf-8 -*-
import hashlib
import hmac
import uuid

import requests

from odoo import models, fields


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("paytrail", "Paytrail")],
        ondelete={"paytrail": "set default"}
    )
    paytrail_merchant_id = fields.Char(string="Merchant Id")
    paytrail_secret_key = fields.Char(string="Secret Key")

    def _paytrail_make_request(self, body):
        # print(fields.Datetime.now().isoformat())
        paytrail_url = "https://services.paytrail.com/payments"
        secret = self.paytrail_secret_key
        headers = dict({
            "checkout-account": self.paytrail_merchant_id,
            "checkout-algorithm": "sha256",
            "checkout-method": "POST",
            "checkout-nonce": str(uuid.uuid4()),
            "checkout-timestamp": str(fields.Datetime.now().isoformat())
            # "checkout-timestamp": "2018-07-06T10:01:31.904Z"
        })
        signature = self.calculate_hmac(secret, headers, body)
        headers["signature"] = signature
        print(headers)
        print(body)
        # response = requests.post(paytrail_url, data=body, headers=headers)
        response = requests.request(method="POST", url=paytrail_url, data=body, headers=headers,
                                    timeout=60)  # (data=body) will only work if its (json=bod)y then there will be signature mismatch
        # Handle Response
        if response.status_code == 201:
            print("\nPayment Created Successfully!")
            print(response.json())  # Should return a payment URL
        else:
            print("\nError:", response.text)

    def calculate_hmac(self, secret, headers, body):
        data = []
        for key, value in headers.items():
            if key.startswith('checkout-'):
                data.append('{key}:{value}'.format(key=key, value=value))
        data.append(body)
        hmac = self.compute_sha256_hash('\n'.join(data), secret)
        return hmac

    def compute_sha256_hash(self, message, secret):
        # whitespaces that were created during json parsing process must be removed
        hash = hmac.new(secret.encode(), message.encode(), digestmod=hashlib.sha256)
        return hash.hexdigest()
