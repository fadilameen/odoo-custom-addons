# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError


class StudentReportWizard(models.TransientModel):
    _name = "student.report.wizard"
    _description = "Student Report Wizard"

    student_ids = fields.Many2many("hostel.student")
    room_ids = fields.Many2many("hostel.room")

    def action_print(self):
        query = """select hostel_student.id, hostel_student.name, total_rent,hostel_student.pending_amount, hostel_room.room_number, hostel_student.invoice_status 
                   from hostel_student FULL JOIN hostel_room on hostel_student.room_id = hostel_room.id WHERE hostel_student.name IS NOT NULL """
        if self.student_ids or self.room_ids:
            # test = self.student_ids.ids
            # print(tuple(test))
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
        print(query)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        data = {
            'report': report,
        }
        if report:
            return self.env.ref(
                'hostel.action_report_hostel_student').report_action(
                self, data=data)
        else:
            raise ValidationError("No records found!")
