from email.policy import default

from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from odoo.exceptions import ValidationError
from odoo.tools import date_utils
from reportlab.graphics.transform import inverse

from odoo import fields
from odoo import api

from odoo import models
from odoo.api import readonly


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        readonly=True,
        string='Status',
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True, )
    property_id = fields.Many2one("estate.property", required=True, )
    validity = fields.Integer(
        default=7,
    )
    date_deadline = fields.Date(
        compute='_date_deadline',
        inverse='_inverse_validity'
    )

    create_date = fields.Date(default=today())

    @api.depends('validity', 'date_deadline', 'create_date')
    def _date_deadline(self):
        for line in self:
            line.date_deadline = date_utils.add(today(), days=line.validity, )

    def _inverse_validity(self):
        for line in self:
            line.validity = (line.date_deadline - line.create_date).days

    @api.depends('property_id')
    def action_accept(self):
        for record in self:
            if 'accepted' not in record.property_id.offer_ids.mapped("status"):
                record.status = 'accepted'
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
            else:
                raise ValidationError("Offer already accepted")

    def action_refuse(self):
        self.status = 'refused'
        if self.property_id.buyer == self.partner_id:
            self.property_id.buyer = ""
            self.property_id.selling_price = 0

    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'accepted':
            print("1")
            # self.action_accept()
            self.property_id.buyer = self.partner_id
            self.property_id.selling_price = self.price
            print("acceptt")

        if self.status == 'refused':
            if self.property_id.buyer == self.partner_id:
                self.property_id.buyer = ""
                self.property_id.selling_price = 0

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price>=0)', 'Offer Price Must be Positive'),
    ]
