/** @odoo-module **/

import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
  set_discount(discount) {
    var res = super.set_discount(discount);
    var discount_limited_category_id =
      this.models["pos.config"].getFirst().pos_category_id.name;
    var product_category_id = this.product_id.pos_categ_ids[0].id;
    var product_categories = [];
    //  console.log(this.product_id.pos_categ_ids[0].name)
    for (let index = 0; index < this.product_id.pos_categ_ids.length; index++) {
      product_categories.push(this.product_id.pos_categ_ids[index].name);
    }
    if (
      product_categories.includes(discount_limited_category_id) &&
      this.models["pos.config"].getFirst().is_category_wise_discount_in_pos
    ) {
      var discount_limit = this.models["pos.config"].getFirst().discount_limit;
      var current_discount = this.discount;
      if (current_discount > discount_limit) {

        window.alert("Enter a valid discount!");
console.log("testtt")
      }
    }
    return res;
  }
});
