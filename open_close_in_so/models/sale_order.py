# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    """model for adding new two state into sale order"""
    _inherit = 'sale.order'

    current_state = fields.Selection(default='open',
                                     selection=[('open', 'Open'),
                                                ('close', 'Close')],
                                     compute='_compute_current_state',
                                     store=True)

    @api.depends("delivery_status")
    def _compute_current_state(self):
        """to compute current state based delivery status"""
        for record in self:
            if record.delivery_status == 'full':
                record.current_state = 'close'
            else:
                record.current_state = record.current_state
