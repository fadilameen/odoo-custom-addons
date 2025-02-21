/** @odoo-module **/

//import { PosStore } from "@point_of_sale/app/store/pos_store";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";



patch(OrderSummary.prototype, {
  _setValue(val) {
  console.log(this)
   this.dialog.add(AlertDialog, {
                title: _t("hehhhheee"),
                body: _t("Suiiiiiiiiiiiiiiiiiiiiiiiii"),
            });
    var res = super._setValue(val);
//    var discount_limited_category_id =
//      this.models["pos.config"].getFirst().pos_category_id.name;
//    var product_category_id = this.product_id.pos_categ_ids[0].id;
//    var product_categories = [];
//    //  console.log(this.product_id.pos_categ_ids[0].name)
//    for (let index = 0; index < this.product_id.pos_categ_ids.length; index++) {
//      product_categories.push(this.product_id.pos_categ_ids[index].name);
//    }
//    if (
//      product_categories.includes(discount_limited_category_id) &&
//      this.models["pos.config"].getFirst().is_category_wise_discount_in_pos
//    ) {
//      var discount_limit = this.models["pos.config"].getFirst().discount_limit;
//      var current_discount = this.discount;
//      if (current_discount > discount_limit) {
//
//        window.alert("Enter a valid discount!");
//console.log("testtt")
//      }
//    }
    return res;
  }
});
