# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.tools import date_utils


class DailyAbsentee(models.Model):
    _name = "daily.absentee"
    _description = "Daily Absentee"

    name = fields.Many2one('hr.employee', string="Employee",
                           required=True, readonly=True)
    date = fields.Date("Date", required=True, readonly=True)

    def create_absentee_list_automatically(self):
        """to create list of absent employees everyday"""
        today = fields.Datetime.today()
        present_employees = self.env['hr.attendance'].search(
            ["&", ("check_in", ">", today),
             ("check_in", "<", date_utils.add(today, days=1))]).employee_id
        all_employees = self.env['hr.employee'].search([])
        # print(all_employees)
        # print(present_employees)
        absent_employees = all_employees.filtered(
            lambda e: e.id not in present_employees.ids)
        # print(absent_employees)
        for employee in absent_employees:
            # print(employee.name)
            # print(employee.id)
            self.create([{'name': employee.id, 'date': today}])
