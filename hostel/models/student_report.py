# -*- coding: utf-8 -*-
"""student report"""
from odoo import models, api


class StudentReport(models.AbstractModel):
    """student report creation abstract model"""
    _name = 'report.hostel.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        """for getting values and passing them to template"""
        docs = self.env['hostel.student'].browse(docids)
        if data.get('report'):
            room_grouping = data['room_grouping']
            data = data['report']
        else:
            room_grouping = False
        return {
            'doc_model': 'hostel.student',
            'docs': docs,
            'data': data,
            'room_grouping': room_grouping,
            'invoice_status_keys': dict(
                self.env['hostel.student']._fields['invoice_status'].selection)
        }
