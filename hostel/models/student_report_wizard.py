# -*- coding: utf-8 -*-
"""student report wizard"""

import io
import json
import xlsxwriter
from odoo.tools import json_default
from odoo import models, fields
from odoo.exceptions import ValidationError


class StudentReportWizard(models.TransientModel):
    """student report wizard"""
    _name = "student.report.wizard"
    _description = "Student Report Wizard"

    student_ids = fields.Many2many("hostel.student")
    room_ids = fields.Many2many("hostel.room")

    def action_pdf(self):
        """To pass values from wizard to report creation"""
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
        report = self.env.cr.dictfetchall()
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
        print("hello")
        students = self.student_ids.search([]).mapped('name')
        print(students)
        data = {
            'students': students
        }
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

    def get_xlsx_report(self, data, response):
        print("get_xlsx_report")
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
        # sheet.merge_range('A4:B4', 'Customer:', cell_format)
        # sheet.merge_range('C4:D4', data['customer'], txt)
        sheet.merge_range('A5:B5', 'Students', cell_format)
        for i, student in enumerate(data['students'],
                                    start=5):  # Start at row 6 for products
            sheet.merge_range(f'C{i}:D{i}', student, txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
