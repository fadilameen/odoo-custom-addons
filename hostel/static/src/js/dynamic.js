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

function uniqueid_generator() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

function getChunkSize() {
    return window.innerWidth < 768 ? 1 : 4;
}

var last_four_rooms = PublicWidget.Widget.extend({
    selector: '.last_four_rooms_snippet',
//    event:{"resize .last_four_rooms_snippet":"chunkDataCheck"},
//    chunkDataCheck:function (ev){
//    console.log('hyy')
//            const newChunkSize = getChunkSize();
//            chunks = _chunk(this.rooms, newChunkSize);
//            chunks[0].is_active = true;
//            refEl.html(renderToElement('hostel.last_four_rooms', {chunks}));
//        },
    willStart: async function () {
        const data = await rpc('/last_four_rooms', {})
        this.rooms = data
    },
    start: function () {
        const chunkSize = getChunkSize();
        var chunks = _chunk(this.rooms, chunkSize);
        console.log(chunks.length)
        if(chunks.length!=0){
        chunks[0].is_active = true
        }
//        chunks.length!=0?chunks[0].is_active = true:false;
        const refEl = this.$el.find("#last_four");
        const unique_id = uniqueid_generator();
        const x = refEl.html(renderToElement('hostel.last_four_rooms', {chunks}));
        const y = this.$el.find(x);
        y.find('.carousel-control-next').attr('href', `#carousel-${unique_id}`);
        y.find('.carousel-control-prev').attr('href', `#carousel-${unique_id}`);
        y.find('#carouselExampleControls').attr('id', `carousel-${unique_id}`);

        window.addEventListener('resize', () => {
        console.log('hyy')
            const newChunkSize = getChunkSize();
            chunks = _chunk(this.rooms, newChunkSize);
            if(chunks.length!=0){
        chunks[0].is_active = true
        }
            refEl.html(renderToElement('hostel.last_four_rooms', {chunks}));
        });
    }
});

PublicWidget.registry.last_four_rooms_snippet = last_four_rooms;
export default last_four_rooms;