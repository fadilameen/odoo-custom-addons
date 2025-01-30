# -*- coding: utf-8 -*-
"""hostel invoice"""
from odoo import fields
from odoo import models


class AccountMove(models.Model):
    """inherited model of hostel invoice"""
    _inherit = "account.move"

    student_id = fields.Many2one("hostel.student", string='Student')

    def action_post(self):
        """overriding action post to send mail automatically"""
        if self.student_id.receive_mail:
            template = self.env.ref(
                'account.email_template_edi_invoice')
            template.send_mail(self.id, force_send=True)
        return super(AccountMove, self).action_post()
