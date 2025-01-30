# -*- coding: utf-8 -*-
"""leave request report"""

from odoo import models, api


class LeaveRequestReport(models.AbstractModel):
    """abstract model of leave request report"""
    _name = 'report.hostel.report_leave_request'

    @api.model
    def _get_report_values(self, docids, data=None):
        """for getting report values"""
        docs = self.env["leave.request"].browse(docids)
        if data.get('report'):
            data = data['report']
        return {
            'doc_ids': docids,
            'doc_model': 'leave.request',
            'docs': docs,
            'data': data,
        }
