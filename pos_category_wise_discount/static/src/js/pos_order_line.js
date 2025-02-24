/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
  setDiscountFromUI(line, val) {
    var res = super.setDiscountFromUI(line, val);
    if (this.models["pos.config"].getFirst().is_category_wise_discount_in_pos) {
      var discount_limited_category =
        this.models["pos.config"].getFirst().pos_category_id.name;
      var product_categories = [];
      for (
        let index = 0;
        index < line.product_id.pos_categ_ids.length;
        index++
      ) {
        product_categories.push(line.product_id.pos_categ_ids[index].name);
      }
      if (product_categories.includes(discount_limited_category)) {
        var discount_limit =
          this.models["pos.config"].getFirst().discount_limit;
        var current_discount = line.discount;
        if (current_discount > discount_limit) {
          this.dialog.add(AlertDialog, {
            title: _t("Alert!"),
            body: _t("Discount exceeded the limit."),
          });
        }
      }
    }
    return res;
  },
});
