# -*- coding: utf-8 -*-
"""student report wizard"""
import io
import json

import xlsxwriter

from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.tools import json_default


class StudentReportWizard(models.TransientModel):
    """student report wizard"""
    _name = "student.report.wizard"
    _description = "Student Report Wizard"

    student_ids = fields.Many2many("hostel.student")
    room_ids = fields.Many2many("hostel.room")
    room_grouping = fields.Boolean(string="Group by Room",
                                   default=False)

    def _get_report_date(self):
        """to fetch values from database"""
        query = """select hostel_student.id, hostel_student.name, total_rent,hostel_student.pending_amount, hostel_room.room_number, hostel_student.invoice_status 
                                from hostel_student FULL JOIN hostel_room on hostel_student.room_id = hostel_room.id WHERE hostel_student.name IS NOT NULL """
        if self.student_ids or self.room_ids:
            if self.student_ids:
                s_ids = tuple(self.student_ids.ids)
                if len(s_ids) == 1:
                    query += """ AND hostel_student.id = %s""" % s_ids
                else:
                    query += """ AND hostel_student.id in %s""" % (s_ids,)
            if self.room_ids:
                r_ids = tuple(self.room_ids.ids)
                if len(r_ids) == 1:
                    query += """ AND hostel_room.id = %s""" % r_ids
                else:
                    query += """ AND hostel_room.id in %s""" % (r_ids,)
        query += """ ORDER BY hostel_room.room_number, hostel_student.name"""
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def action_pdf(self):
        """To pass values from wizard to report creation"""
        report = self._get_report_date()
        data = {'report': report,
                'room_grouping': self.room_grouping}
        if report:
            return self.env.ref(
                'hostel.action_report_hostel_student').report_action(
                self, data=data)
        else:
            raise ValidationError("No records found!")

    def action_xlsx(self):

        """To pass values from wizard to report creation"""
        report = self._get_report_date()
        data = {'report': report,
                'room_grouping': self.room_grouping}
        if report:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'student.report.wizard',
                         'options': json.dumps(data,
                                               default=json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Student Excel Report',
                         },
                'report_type': 'xlsx',
            }
        else:
            raise ValidationError("No records found!")

    def get_xlsx_report(self, data, response):
        """defining the structure of xlsx and values"""
        room_grouping = data['room_grouping']
        data = data['report']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('G2:J3', 'STUDENT REPORT', head)
        sheet.merge_range('C5:D5', 'SL No', cell_format)
        sheet.merge_range('E5:F5', 'Name', cell_format)
        sheet.merge_range('G5:H5', 'Monthly Rent', cell_format)
        sheet.merge_range('I5:J5', 'Pending Amount', cell_format)
        sheet.merge_range('K5:L5', 'Room', cell_format)
        sheet.merge_range('M5:N5', 'Invoice Status', cell_format)

        current_room = None
        row = 6
        sl_no = 1
        for student in data:
            if not student['room_number']:
                student['room_number'] = "None"
            if room_grouping and student['room_number'] != current_room:
                if row != 6:
                    sheet.merge_range(f'C{row}:N{row}', "")
                    row += 1
                sheet.write(f'B{row}', student['room_number'], cell_format)

            sheet.merge_range(f'C{row}:D{row}', sl_no, txt)
            sheet.merge_range(f'E{row}:F{row}', student['name'], txt)
            sheet.merge_range(f'G{row}:H{row}', student['total_rent'], txt)
            sheet.merge_range(f'I{row}:J{row}', student['pending_amount'], txt)
            sheet.merge_range(f'K{row}:L{row}', student['room_number'], txt)
            sheet.merge_range(f'M{row}:N{row}',
                              dict(self.student_ids._fields[
                                       'invoice_status'].selection).get(
                                  student['invoice_status']), txt)
            current_room = student['room_number']
            row += 1
            sl_no += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
