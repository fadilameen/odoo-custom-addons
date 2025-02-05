/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";
export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
var TopSellingProducts = PublicWidget.Widget.extend({
        selector: '.best_seller_product_snippet',
        willStart: async function () {
            const data = await jsonrpc('/last_four_rooms', {})
            const [products, categories, website_id, unique_id] = data
            Object.assign(this, {
                products, categories, website_id, unique_id
            })
        },
        start: function () {
            const refEl = this.$el.find("#top_products_carousel")
            const { products, categories, current_website_id, products_list} = this
            const chunkData = chunk(products, 4)
            refEl.html(renderToElement(module_name.products_category_wise', {
                products,
                categories,
                current_website_id,
                products_list,
                chunkData
            }))
        }
    });
PublicWidget.registry.products_category_wise_snippet = TopSellingProducts;
return TopSellingProducts;