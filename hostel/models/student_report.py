# -*- coding: utf-8 -*-

from odoo import models, api


class StudentReport(models.AbstractModel):
    _name = 'report.hostel.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hostel.student'].browse(docids)

        print(docs)
        if data.get('report'):
            data = data['report']
        return {
            # 'doc_ids': docs.ids,
            'doc_model': 'hostel.student',
            'docs': docs,
            'data': data,
        }
