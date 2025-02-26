/** @odoo-module **/

import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
  getDisplayData() {
    const data = super.getDisplayData();
    if (this.product_id.brand) {
      data.brand = this.product_id.brand;
    }
    return data;
  },
});
