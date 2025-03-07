# -*- coding: utf-8 -*-
import json
import uuid

from dateutil.utils import today
from werkzeug import urls
from odoo import models, fields


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'paytrail':
            return res
        payload = self._paytrail_prepare_payment_request_payload()
        self.provider_id._paytrail_make_request(payload)

    def _paytrail_prepare_payment_request_payload(self):
        base_url = self.get_base_url()
        redirect_url = urls.url_join(base_url, '/contactus-thank-you')
        # print(self.read())
        body = dict({
            "stamp": str(uuid.uuid4()),
            "reference": self.reference,
            "amount": self.amount,
            "currency": "EUR",
            "language": 'EN',
            "items": [{"unitPrice": self.amount, "units": 1, "vatPercentage": 0, "productCode": "#1234",
                       "deliveryDate": str(fields.Date.today())}],
            "customer": {"email": self.partner_email},
            "redirectUrls": {"success": redirect_url, "cancel": redirect_url}
        })
        payload = json.dumps(body, separators=(',', ':'))
        # print(body_json)
        return payload
