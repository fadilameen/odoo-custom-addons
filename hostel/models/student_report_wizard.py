# -*- coding: utf-8 -*-
from odoo import models, fields


class StudentReportWizard(models.TransientModel):
    _name = "student.report.wizard"
    _description = "Student Report Wizard"

    def action_print(self):
        students = self.env['hostel.student'].search([])
        data = {
            'student_ids': students.ids,
        }
        return self.env.ref(
            'hostel.action_report_hostel_student').report_action(
            self, data=data)
