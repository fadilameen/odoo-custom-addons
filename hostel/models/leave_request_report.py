# -*- coding: utf-8 -*-
"""leave request report"""

from odoo import models, api


class LeaveRequestReport(models.AbstractModel):
    """abstract model of leave request report"""
    _name = 'report.hostel.report_leave_request'
    _description = "Leave Request Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """for getting report values"""
        docs = self.env["leave.request"].browse(docids)
        if data.get('report'):
            student_grouping = data['student_grouping']
            data = data['report']
        else:
            student_grouping = False
        return {
            'doc_ids': docids,
            'doc_model': 'leave.request',
            'docs': docs,
            'data': data,
            'student_grouping': student_grouping
        }
