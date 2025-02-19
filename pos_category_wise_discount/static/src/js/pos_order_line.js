/** @odoo-module **/

import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

    patch(PosOrderline.prototype, {
        getDisplayData() {
             var res=super.getDisplayData();
             console.log(this.models["pos.config"].getFirst().pos_category_id)
             return res
        }
    });
