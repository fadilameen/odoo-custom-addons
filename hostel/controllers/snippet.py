# -*- coding: utf-8 -*-
from odoo import http


class DynamicSnippets(http.Controller):
    """This class is for the getting values for dynamic product snippets"""

    @http.route('/last_four_rooms', type='json', auth='public')
    def last_four_rooms(self):
        print("last four")
