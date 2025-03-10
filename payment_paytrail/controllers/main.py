# -*- coding: utf-8 -*-

import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PaytrailController(http.Controller):
    _return_url = '/payment/paytrail/return'

    @http.route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False, save_session=False)
    def paytrail_return_from_checkout(self, **data):
        """ Process the notification data sent by Paytrail after redirection from checkout."""
        print(data)
        _logger.info("handling redirection from Paytrail with data:\n%s", pprint.pformat(data))
        request.env['payment.transaction'].sudo()._handle_notification_data('paytrail', data)
        return request.redirect('/payment/status')
