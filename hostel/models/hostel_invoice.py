# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    student_id = fields.Many2one("hostel.student", string='Student')

    def action_post(self):
        print("hello invoice")
        if self.student_id.receive_mail:
            print("mail")
            template = self.env.ref(
                'account.email_template_edi_invoice')
            print(self.id)
            template.send_mail(self.id, force_send=True)
        else:
            print("no mail")
        return super(AccountMove, self).action_post()
