# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSaleInherit(WebsiteSale):
    @http.route(['/shop/cart', ], type='http', auth="public", website=True)
    def cart(self, access_token=None, revive='', **post):
        res = super(WebsiteSaleInherit, self).cart(access_token, revive, **post)
        print(res)
        print(res.qcontext)
        bom_product_ids = eval(
            request.env['ir.config_parameter'].sudo().get_param(
                'bom_in_cart.bom_product_ids'))
        res.qcontext.update({'bom_product_ids': bom_product_ids})
        print(res.qcontext)
        return res
