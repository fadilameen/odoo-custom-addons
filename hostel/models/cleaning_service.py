from email.policy import default

from odoo import fields, models


class CleaningService(models.Model):
    _name = "cleaning.service"
    _description = "Cleaning Service"
    _rec_name = "room_id"

    room_id = fields.Many2one("hostel.room", required=True)
    start_time = fields.Datetime(string="Start Time")
    cleaning_staff = fields.Many2one("res.users")
    state = fields.Selection(
        selection=[('new', 'New'), ('assigned', 'Assigned'), ('done', 'Done')],
        default='new')
    company_id = fields.Many2one('res.company',
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)

    def action_assign_cleaning_service(self):
        # print(self.env.user.name)
        self.cleaning_staff = self.env.user
        self.state = "assigned"

    def action_complete(self):
        self.state = "done"
        self.room_id.compute_current_state()
