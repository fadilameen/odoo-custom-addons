# -*- coding: utf-8 -*-

from odoo import models, api


class LeaveRequestReport(models.AbstractModel):
    _name = 'report.hostel.report_leave_request'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["leave.request"].browse(docids)
        if data.get('report'):
            data = data['report']
        return {
            'doc_ids': docids,
            'doc_model': 'leave.request',
            'docs': docs,
            'data': data,
        }
