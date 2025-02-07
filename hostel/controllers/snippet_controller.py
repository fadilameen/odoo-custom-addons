# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class DynamicSnippets(http.Controller):
    """This class is for the getting values for dynamic product snippets"""

    @http.route('/last_four_rooms', type='json', auth='public')
    def last_four_rooms(self):
        rooms = request.env['hostel.room'].sudo().search_read([],
                                                              ['room_number',
                                                               'room_type',
                                                               'bed_count',
                                                               'person_count',
                                                               'image'],
                                                              order='id desc',
                                                              limit=4)
        room_type = dict(
            request.env['hostel.room']._fields['room_type'].selection)
        print(rooms, room_type)
        return rooms, room_type

    @http.route('/store/<model("hostel.room"):room>', type='http', auth="user",
                website=True)
    def room_details(self, room):
        values = {
            'room': room,
        }
        # print(room.read())
        return request.render('hostel.room_details', values)
