# -*- coding: utf-8 -*-
"""leave request report wizard"""
from odoo import models, fields
from odoo.exceptions import ValidationError


class LeaveRequestReportWizard(models.TransientModel):
    """leave request report wizard"""
    _name = "leave.request.report.wizard"
    _description = "Leave Request Report Wizard"

    student_ids = fields.Many2many("hostel.student")
    room_ids = fields.Many2many("hostel.room")
    leave_date = fields.Date()
    arrival_date = fields.Date()

    def action_print(self):
        """To pass values from wizard to report creation"""
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
        report = self.env.cr.dictfetchall()
        data = {'report': report}
        if report:
            return self.env.ref(
                'hostel.action_report_leave_request').report_action(
                self, data=data)
        else:
            raise ValidationError("No records found!")
