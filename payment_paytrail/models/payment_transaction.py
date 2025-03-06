# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import uuid

from odoo import models, fields


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):
        # print(processing_values, "processing values")
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'paytrail':
            return res
        self._get_paytrail_request(processing_values)
        return res

    # def _get_paytrail_items(self, processing_value):
    #     items = []
    #     for sale_order in self.sale_order_ids:
    #         for order_line in (sale_order.order_line):
    #             print(order_line.read())
    #             # items += {
    #             #     "unitPrice": order_line.price_unit,
    #             #     "units": order_line.product_qty,
    #             #     "vatPercentage": 25.5,
    #             #     "productCode": "#1234",
    #             #     "deliveryDate": "2018-09-01",
    #             # }
    def calculate_hmac(self, secret: str, headerParams, body):
        data = []
        for key, value in headerParams.items():
            if key.startswith('checkout-'):
                data.append('{key}:{value}'.format(key=key, value=value))
        data.append(body)
        print(data)
        print(self.compute_sha256_hash('\n'.join(data), secret))

    def compute_sha256_hash(self, message, secret):
        # whitespaces that were created during json parsing process must be removed
        hash = hmac.new(secret.encode(), message.encode(), digestmod=hashlib.sha256)
        return hash.hexdigest()

    def _get_paytrail_request(self, processing_values):
        # print(self.read(), "read")
        # items = self._get_paytrail_items(processing_values)
        headers = self.provider_id._prepare_paytrail_header()
        body = {
            "stamp": str(uuid.uuid4()),
            "reference": self.reference,
            "amount": self.amount,
            "currency": self.currency_id.name,
            "language": "EN",
            "items": [
                {
                    "unitPrice": self.amount,
                    "units": 1,
                    "vatPercentage": 0,
                    "productCode": "#1",
                    "deliveryDate": str(fields.Datetime.today()),
                },
            ],
            "customer": {
                "email": self.partner_email,
            },
            "redirectUrls": {
                "success": "http://localhost:8018/shop/payment/success",
                "cancel": "http://localhost:8018/shop/payment/cancel",
            },
        }
        body_json = json.dumps(body, separators=(',', ':'))
        encData = self.calculate_hmac(self.provider_id.paytrail_secret_key, headers, body_json)
        # print("Encrypted data: " + encData)
        # print(body)
        # print(body_json)
