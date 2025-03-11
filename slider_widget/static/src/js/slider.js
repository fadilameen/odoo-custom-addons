/** @odoo-module **/
import { Component } from "@odoo/owl";
import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
export class RangeSliderField extends Component {
  static template = 'SliderWidget';
  setup(){
       const {min,max,step=0.1} = this.__owl__.parent.props.fieldInfo.attrs
         console.log(min,max)
         console.log(this)

       this.state = useState({
           value : this.props.record.data[this.props.name],
           min : min,
           max : max,
           step: step,
       });
  }
  getValue(e) {
       const config = this.env.model.config
       this.state.value = e.srcElement.value
       this.env.model.orm.write(config.resModel,
                               [config.resId], {
                               [this.props.name]: this.state.value,
       });
       console.log(config)
  }
}
export const rangeSliderField = {
   component: RangeSliderField,
   displayName: "RangeSliderField",
   supportedTypes: ["float"],
};
registry.category("fields").add("RangeSliderField", rangeSliderField);
