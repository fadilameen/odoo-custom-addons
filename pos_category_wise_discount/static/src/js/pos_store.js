/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
  pay() {
    if (this.models["pos.config"].getFirst().is_category_wise_discount_in_pos) {
      var discount_limited_category =
        this.models["pos.config"].getFirst().pos_category_id.name;
      var order_lines = this.get_order().get_orderlines();
      var current_total_amount = 0;
      var actual_total_amount = 0;
      order_lines.forEach((line) => {
        var categories = [];
        line.product_id.pos_categ_ids.forEach((category) => {
          categories.push(category.name);
        });
        if (categories.includes(discount_limited_category)) {
          current_total_amount += line.price_subtotal;
          actual_total_amount += line.price_unit * line.qty;
        }
      });
      var allowed_total =
        actual_total_amount -
        (actual_total_amount *
          this.models["pos.config"].getFirst().discount_limit) /
          100;
      if (current_total_amount < allowed_total) {
        this.dialog.add(AlertDialog, {
          title: _t("Alert!"),
          body: _t("Category discount exceeded the limit."),
        });
      } else {
        super.pay();
      }
    } else {
      super.pay();
    }
  },
});
