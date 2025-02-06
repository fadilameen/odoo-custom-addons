/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";
var last_four_rooms = PublicWidget.Widget.extend({
        selector: '.last_four_rooms_snippet',
        willStart: async function () {
            const data = await rpc('/last_four_rooms', {})
            const rooms = data
            Object.assign(this, {
                rooms
            })
        },
        start: function () {

            const refEl = this.$el.find("#last_four")
            const rooms = this.rooms
            const x=refEl.html(renderToElement('hostel.last_four_rooms', {rooms}))
//            console.log(,"xxx")
        }
    });
PublicWidget.registry.last_four_rooms_snippet = last_four_rooms;
return last_four_rooms;



