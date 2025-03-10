# -*- coding: utf-8 -*-
import json
import logging
import uuid

from werkzeug import urls

from odoo import models, fields, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):
        """overriding payment and adding logic for custom payment method"""
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'paytrail':
            return res
        payload = self._paytrail_prepare_payment_request_payload()
        payment_response = self.provider_id._paytrail_make_request(payload)
        self.provider_reference = payment_response.get('reference')
        redirect_form_html = self.env['ir.qweb']._render('payment_paytrail.redirect_form_paytrail', {
            'payment_url': payment_response['href'],
        })
        processing_values.update({
            'api_url': payment_response['href'],
            'redirect_form_html': redirect_form_html,
        })
        return processing_values

    def _paytrail_prepare_payment_request_payload(self):
        """to generate payload"""
        amount_in_euro = self.amount * self.env['res.currency'].search([("name", "=", "EUR")]).rate
        base_url = self.get_base_url()
        redirect_url = urls.url_join(base_url, '/payment/paytrail/return')
        body = dict({
            "stamp": str(uuid.uuid4()),
            "reference": self.reference,
            "amount": int(amount_in_euro * 100),
            "currency": "EUR",
            "language": 'EN',
            "items": [{"unitPrice": int(amount_in_euro * 100), "units": 1, "vatPercentage": 0, "productCode": "#1234",
                       "deliveryDate": str(fields.Date.today())}],
            "customer": {"email": self.partner_email},
            "redirectUrls": {"success": redirect_url, "cancel": redirect_url}
        })
        payload = json.dumps(body, separators=(',', ':'))
        return payload

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Find the transaction based on the notification data.

          For a provider to handle transaction processing, it must overwrite this method and return
          the transaction matching the notification data.

          :param str provider_code: The code of the provider handling the transaction.
          :param dict notification_data: The notification data sent by the provider.
          :return: The transaction, if found.
          :rtype: recordset of `payment.transaction`
          """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'paytrail' or len(tx) == 1:
            return tx
        tx = self.search(
            [('reference', '=', notification_data.get('checkout-reference')), ('provider_code', '=', 'paytrail')]
        )
        if not tx:
            raise ValidationError("Paytrail: " + _(
                "No transaction found matching reference %s.", notification_data.get('checkout-reference')
            ))
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Mollie data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """
        super()._process_notification_data(notification_data)

        if self.provider_code != 'paytrail':
            return
        payment_status = notification_data.get('checkout-status')
        if payment_status in ['pending', 'delayed']:
            self._set_pending()
        elif payment_status == 'ok':
            self._set_done()
        elif payment_status in ['fail']:
            self._set_canceled("Paytrail: " + _("Cancelled payment with status: %s", payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "Paytrail: " + _("Received data with invalid payment status: %s", payment_status)
            )
