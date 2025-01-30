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
            data = data['report']
        return {
            'doc_model': 'hostel.student',
            'docs': docs,
            'data': data,
        }
