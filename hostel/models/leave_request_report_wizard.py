# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError


class LeaveRequestReportWizard(models.TransientModel):
    _name = "leave.request.report.wizard"
    _description = "Leave Request Report Wizard"

    student_ids = fields.Many2many("hostel.student")
    room_ids = fields.Many2many("hostel.room")
    leave_date = fields.Date()
    arrival_date = fields.Date()

    def action_print(self):
        query = """select hs.name,hr.room_number,lr.leave_date,lr.arrival_date ,lr.duration
        from leave_request lr inner join hostel_student hs on lr.student_name=hs.id 
        inner join hostel_room hr on hs.room_id=hr.id"""
        where_added = False
        print(self.leave_date)
        if self.student_ids:
            ids = tuple(self.student_ids.ids)
            if len(ids) == 1:
                query += """ WHERE hs.id = %s""" % ids
            else:
                query += """ WHERE hs.id in %s""" % (ids,)
            where_added = True
        if self.room_ids:
            ids = tuple(self.room_ids.ids)
            if len(ids) == 1:
                if where_added:
                    query += """ AND hr.id = %s""" % ids
                else:
                    query += """ WHERE hr.id = %s""" % ids
            else:
                if where_added:
                    query += """ AND hr.id in %s""" % (ids,)
                else:
                    query += """ WHERE hr.id in %s""" % (ids,)
            where_added = True
        if self.leave_date:
            if where_added:
                query += """ AND lr.leave_date =  '%s'""" % self.leave_date
            else:
                query += """ WHERE lr.leave_date =  '%s'""" % self.leave_date
        where_added = True
        if self.arrival_date:
            if where_added:
                query += """ AND lr.arrival_date =  '%s'""" % self.arrival_date
            else:
                query += """ WHERE lr.arrival_date =  '%s'""" % self.arrival_date
        print(query)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        # print(report)
        data = {'report': report}
        if report:
            return self.env.ref(
                'hostel.action_report_leave_request').report_action(
                self, data=data)
        else:
            raise ValidationError("No records found!")
