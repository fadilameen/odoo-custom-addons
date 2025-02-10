/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";
export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
var last_four_rooms = PublicWidget.Widget.extend({
        selector: '.last_four_rooms_snippet',
        willStart: async function () {
            const data = await rpc('/last_four_rooms', {})
            const rooms = data
//            Object.assign(this, {
//                rooms
//            })
            this.rooms=rooms
//            console.log(rooms,"rooms")
        },
        start: function () {
            var chunks = _chunk(this.rooms, 4)
            chunks[0].is_active = true
            console.log({chunks},"chunks")
            const refEl = this.$el.find("#last_four")
            const rooms = this.rooms
            console.log("data going ",{rooms})
            const x=refEl.html(renderToElement('hostel.last_four_rooms', {chunks}))
        }
    });
PublicWidget.registry.last_four_rooms_snippet = last_four_rooms;
return last_four_rooms;



