# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo.http import request, Controller, route


class WebFormController(Controller):
    @route('/hostel', type='http', auth='public', website=True)
    def hostel_form(self):
        return request.render("hostel.online_hostel_form",
                              {'rooms': request.env['hostel.room'].search(
                                  [("state", "in",
                                    ["empty", "partial"])])})

    @route('/hostel/submit', type='http', auth='public', website=True,
           methods=['POST'])
    def hostel_form_submit(self, **post):
        room = request.env['hostel.room'].browse(int(post.get('room')))
        if room.state in ["empty", "partial"]:
            request.env['hostel.student'].sudo().create({
                'name': post.get('name'),
                'email': post.get('email'),
                'room_id': room.id,
            })
        else:
            raise ValidationError("Sorry the room is already full")

        return request.redirect('/contactus-thank-you')
