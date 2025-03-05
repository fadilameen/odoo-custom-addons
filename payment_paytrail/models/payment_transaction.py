# -*- coding: utf-8 -*-
from odoo import models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):
        # print("function _get_specific_processing_values")
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'paytrail':
            return res
        self._get_paytrail_request(processing_values)
        return res

    def _get_paytrail_request(self, processing_values):
        # print(self.read())
        header = self.provider_id._prepare_paytrail_header()
        print(header)
