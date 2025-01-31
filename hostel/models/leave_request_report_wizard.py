# -*- coding: utf-8 -*-
"""leave request report wizard"""
import io
import json

import xlsxwriter

from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.tools import json_default


class LeaveRequestReportWizard(models.TransientModel):
    """leave request report wizard"""
    _name = "leave.request.report.wizard"
    _description = "Leave Request Report Wizard"

    student_ids = fields.Many2many("hostel.student")
    room_ids = fields.Many2many("hostel.room")
    leave_date = fields.Date()
    arrival_date = fields.Date()

    def _get_report_data(self):
        """to fetch values from database"""
        query = """select hs.name,hr.room_number,lr.leave_date,lr.arrival_date ,lr.duration
               from leave_request lr inner join hostel_student hs on lr.student_name=hs.id 
               inner join hostel_room hr on hs.room_id=hr.id WHERE 1=1"""
        if self.student_ids:
            ids = tuple(self.student_ids.ids)
            if len(ids) == 1:
                query += """ AND hs.id = %s""" % ids
            else:
                query += """ AND hs.id in %s""" % (ids,)
        if self.room_ids:
            ids = tuple(self.room_ids.ids)
            if len(ids) == 1:
                query += """ AND hr.id = %s""" % ids
            else:
                query += """ AND hr.id in %s""" % (ids,)
        if self.leave_date:
            query += """ AND lr.leave_date =  '%s'""" % self.leave_date
        if self.arrival_date:
            query += """ AND lr.arrival_date =  '%s'""" % self.arrival_date
        query += """ ORDER BY hs.name,hr.room_number"""
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def action_pdf(self):
        """To pass values from wizard to report creation"""
        report = self._get_report_data()
        data = {'report': report}
        if report:
            return self.env.ref(
                'hostel.action_report_leave_request').report_action(
                self, data=data)
        else:
            raise ValidationError("No records found!")

    def action_xlsx(self):
        """To pass values from wizard to report creation"""
        report = self._get_report_data()
        data = {'report': report}
        if report:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'leave.request.report.wizard',
                         'options': json.dumps(data['report'],
                                               default=json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Leave Request Report',
                         },
                'report_type': 'xlsx',
            }
        else:
            raise ValidationError("No records found!")

    def get_xlsx_report(self, data, response):
        """defining the structure of xlsx and values"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('F2:K3', 'LEAVE REQUEST REPORT', head)
        sheet.merge_range('C5:D5', 'SL No', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'C{i}:D{i}', i - 5, txt)

        sheet.merge_range('E5:F5', 'Name', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'E{i}:F{i}', student['name'], txt)

        sheet.merge_range('G5:H5', 'Monthly Rent', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'G{i}:H{i}', student['room_number'], txt)

        sheet.merge_range('I5:J5', 'Pending Amount', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'I{i}:J{i}', student['leave_date'], txt)

        sheet.merge_range('K5:L5', 'Room', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'K{i}:L{i}', student['arrival_date'], txt)

        sheet.merge_range('M5:N5', 'Invoice Status', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'M{i}:N{i}', student['duration'], txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
