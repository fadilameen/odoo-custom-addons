# -*- coding: utf-8 -*-
from odoo import models, fields


class StudentReportWizard(models.TransientModel):
    _name = "student.report.wizard"
    _description = "Student Report Wizard"

    student_ids = fields.Many2many("hostel.student")
    room_ids = fields.Many2many("hostel.room")

    def action_print(self):
        query = """select hostel_student.id, hostel_student.name, total_rent,hostel_student.pending_amount, hostel_room.room_number, hostel_student.invoice_status 
                   from hostel_student FULL JOIN hostel_room on hostel_student.room_id = hostel_room.id"""
        if self.student_ids or self.room_ids:
            # test = self.student_ids.ids
            # print(tuple(test))
            where_added = False

            if self.student_ids:
                ids = tuple(self.student_ids.ids)
                if len(ids) == 1:
                    query += """ WHERE hostel_student.id = %s""" % ids
                else:
                    query += """ WHERE hostel_student.id in %s""" % (ids,)
                where_added = True
            if self.room_ids:
                ids = tuple(self.room_ids.ids)
                if len(ids) == 1:
                    if where_added:
                        query += """ AND hostel_room.id = %s""" % ids
                    else:
                        query += """ WHERE hostel_room.id = %s""" % ids
                else:
                    if where_added:
                        query += """ AND hostel_room.id in %s""" % (ids,)
                    else:
                        query += """ WHERE hostel_room.id in %s""" % (ids,)
        # print(query)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        # print(report)
        data = {
            'report': report,
        }
        return self.env.ref(
            'hostel.action_report_hostel_student').report_action(
            self, data=data)
