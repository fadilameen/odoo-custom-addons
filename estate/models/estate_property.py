from email.policy import default

from dateutil.utils import today

from odoo.api import readonly
from odoo.exceptions import ValidationError, UserError
from odoo.tools import date_utils
from odoo import models, api
from odoo import fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    name = fields.Char(required=True)
    description = fields.Text()
    type = fields.Many2one("estate.property.type")
    active = fields.Boolean('Active', default=True)
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=date_utils.add(today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),

        ],
        string='Status',
        copy=False,
        default='new',
    )
    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tags = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", 'property_id')
    total_area = fields.Float(compute='_total_area')
    best_price = fields.Integer(compute='_best_price')

    @api.depends('garden_area', 'living_area')
    def _total_area(self):
        for line in self:
            line.total_area = line.garden_area + line.living_area

    @api.depends('offer_ids')
    def _best_price(self):
        for offer in self:
            if offer.offer_ids:
                offer.best_price = max(offer.offer_ids.mapped('price'))
            else:
                offer.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_set_sold(self):
        if self.state == 'cancelled':
            raise UserError("You Cannot Sell a cancelled Property")
        else:
            self.state = 'sold'

    def action_set_cancelled(self):
        if self.state == 'sold':
            raise UserError("You Cannot Cancel a Sold Property")
        else:
            self.state = 'cancelled'

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price>=0)', 'Expected Price Must be Positive'),
        ('positive_selling_price', 'CHECK(selling_price>=0)', 'Selling Price Must be Positive')
    ]
