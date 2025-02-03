from odoo.http import request, Controller, route


class WebFormController(Controller):
    @route('/hostel', auth='public', website=True)
    def hostel_form(self):
        return request.render("hostel.online_hostel_form")

    @route('/hostel/submit', type='http', auth='public', website=True,
           methods=['POST'])
    def hostel_form_submit(self, **post):
        request.env['hostel.student'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
        })
        return request.redirect('/thank-you-page')
