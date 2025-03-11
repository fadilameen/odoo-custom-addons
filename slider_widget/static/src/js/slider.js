/** @odoo-module **/
import { Component } from "@odoo/owl";
import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class RangeSliderField extends Component {
  static template = 'SliderWidget';
   static props = {
        ...standardFieldProps,
        min: { type: Number, optional: true },
        max: { type: Number, optional: true },
        step: { type: Number, optional: true },
    };
   static defaultProps = {
        min: 0,
        max: 10,
        min: 1,

    };
  setup(){
       const {min,max,step} = this.__owl__.parent.props.fieldInfo.attrs
         console.log(min,max,step)
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
  }
}

export const rangeSliderField = {
   component: RangeSliderField,
   displayName: "RangeSliderField",
    supportedOptions: [
        {
            label: _t("Minimum Value"),
            name: "minimum_value",
            type: "number",
        },
          {
            label: _t("Maximum Value"),
            name: "maximum_value",
            type: "number",
        },
           {
            label: _t("Step"),
            name: "step",
            type: "number",
        },
    ],
   supportedTypes: ["float"],
       extractProps: ({ attrs, options }) => ({
        min: options.minimum_value,
        max: options.maximum_value,
        step: options.step
    }),
};
registry.category("fields").add("RangeSliderField", rangeSliderField);
