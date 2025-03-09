# -*- coding: utf-8 -*-
import json
import uuid
from werkzeug import urls
from odoo import models, fields


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'paytrail':
            return res
        payload = self._paytrail_prepare_payment_request_payload()
        payment_response = self.provider_id._paytrail_make_request(payload)
        self.provider_reference = payment_response.get('reference')  # You already have this
        transaction_id = payment_response.get('transactionId')  # Store this too
        print(payment_response)
        # Create an HTML form for the redirect
        redirect_form_html = f'''
            <form method="GET" action="{payment_response['href']}">
                <!-- You can add hidden fields here if needed -->
            </form>
        '''

        processing_values.update({
            'redirect_form_html': redirect_form_html,
            'api_url': payment_response['href'],
        })
        return processing_values

    # def _get_specific_rendering_values(self, processing_values):
    #     print('helloooo')
    #     res = super()._get_specific_rendering_values(processing_values)

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
