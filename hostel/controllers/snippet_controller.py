# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class DynamicSnippets(http.Controller):
    """This class is for the getting values for dynamic product snippets"""

    @http.route('/last_four_rooms', type='json', auth='public')
    def last_four_rooms(self):
        rooms = request.env['hostel.room'].search_read([], ['room_number',
                                                            'bed_count'],
                                                       order='id',
                                                       limit=4)
        rooms = sorted(rooms, key=lambda i: i['id'],
                       reverse=True)
        print(rooms)
        return rooms
