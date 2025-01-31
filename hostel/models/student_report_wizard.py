# -*- coding: utf-8 -*-
"""student report wizard"""
import io
import json
import xlsxwriter
from odoo.tools import date_utils, json_default
from odoo import models, fields
from odoo.exceptions import ValidationError


class StudentReportWizard(models.TransientModel):
    """student report wizard"""
    _name = "student.report.wizard"
    _description = "Student Report Wizard"

    student_ids = fields.Many2many("hostel.student")
    room_ids = fields.Many2many("hostel.room")

    def _get_report_date(self):
        """to fetch values from database"""
        query = """select hostel_student.id, hostel_student.name, total_rent,hostel_student.pending_amount, hostel_room.room_number, hostel_student.invoice_status 
                                from hostel_student FULL JOIN hostel_room on hostel_student.room_id = hostel_room.id WHERE hostel_student.name IS NOT NULL """
        if self.student_ids or self.room_ids:
            if self.student_ids:
                ids = tuple(self.student_ids.ids)
                if len(ids) == 1:
                    query += """ AND hostel_student.id = %s""" % ids
                else:
                    query += """ AND hostel_student.id in %s""" % (ids,)
            if self.room_ids:
                ids = tuple(self.room_ids.ids)
                if len(ids) == 1:
                    query += """ AND hostel_room.id = %s""" % ids
                else:
                    query += """ AND hostel_room.id in %s""" % (ids,)
        query += """ ORDER BY hostel_room.room_number, hostel_student.name"""
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def action_pdf(self):
        """To pass values from wizard to report creation"""
        report = self._get_report_date()
        data = {
            'report': report,
        }
        if report:
            return self.env.ref(
                'hostel.action_report_hostel_student').report_action(
                self, data=data)
        else:
            raise ValidationError("No records found!")

    def action_xlsx(self):
        """To pass values from wizard to report creation"""
        report = self._get_report_date()
        data = {
            'report': report,
        }
        if report:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'student.report.wizard',
                         'options': json.dumps(data['report'],
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
        print(data)
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
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'C{i}:D{i}', i - 5, txt)

        sheet.merge_range('E5:F5', 'Name', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'E{i}:F{i}', student['name'], txt)

        sheet.merge_range('G5:H5', 'Monthly Rent', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'G{i}:H{i}', student['total_rent'], txt)

        sheet.merge_range('I5:J5', 'Pending Amount', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'I{i}:J{i}', student['pending_amount'], txt)

        sheet.merge_range('K5:L5', 'Room', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'K{i}:L{i}', student['room_number'], txt)

        sheet.merge_range('M5:N5', 'Invoice Status', cell_format)
        for i, student in enumerate(data, start=6):
            sheet.merge_range(f'M{i}:N{i}', student['invoice_status'], txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
