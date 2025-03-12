/** @odoo-module **/
import { Component } from "@odoo/owl";
import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class RangeSliderField extends Component {
  static template = "SliderWidget";
  static props = {
    ...standardFieldProps,
    min: { type: Number, optional: true },
    max: { type: Number, optional: true },
    step: { type: Number, optional: true },
    color: { type: String, optional: true },
  };
  static defaultProps = {
    min: 0,
    max: 10,
    step: 1,
    color: "blue",
  };
  setup() {
    this.state = useState({
      value: this.props.record.data[this.props.name] ?? this.props.min,
      min: this.props.min,
      max: this.props.max,
      step: this.props.step,
      color: this.props.color,
    });
  }
  getValue(e) {
    const config = this.env.model.config;
    this.state.value = e.srcElement.value;
    this.env.model.orm.write(config.resModel, [config.resId], {
      [this.props.name]: this.state.value,
    });
  }
}

export const rangeSliderField = {
  component: RangeSliderField,
  displayName: "RangeSliderField",
  supportedTypes: ["float"],
  extractProps: ({ attrs, options }) => ({
    min: options.minimum_value,
    max: options.maximum_value,
    step: options.step,
    color: options.color,
  }),
};
registry.category("fields").add("RangeSliderField", rangeSliderField);
