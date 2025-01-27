import logging

from odoo import models, api

_logger = logging.getLogger(__name__)


class StudentReport(models.AbstractModel):
    _name = 'report.hostel.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        # print("self====", self, )
        # print("docids===", docids)
        if data and data.get('student_ids'):
            # print("data===", data['student_ids'])
            docs = self.env['hostel.student'].browse(data['student_ids'])
            # print(docs)
        else:
            docs = self.env['hostel.student'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'hostel.student',
            'docs': docs,
            'data': data,
        }
