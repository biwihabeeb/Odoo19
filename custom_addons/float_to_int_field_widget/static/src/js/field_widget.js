/** odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useInputField } from "@web/views/fields/input_field_hook";
import { useRef, onWillRender, onMounted } from "@odoo/owl";

export class FloatToInt extends Component {
    setup() {
        this.input = useRef("input_field");
        useInputField({
            getValue: () => this.props.record.data[this.props.name] || "",
            refName: "input_field",
        });
        onWillRender(() => {
            this.rounded()
        });
        onMounted(() => {
            this.rounded()
        });
    }
    rounded() {
        console.log('Props: ',this.props)
        if (this.input.el){
            console.log('Fraction');
            this.props.record.data[this.props.name] = Math.round(this.input.el.value);
            console.log('value ',this.input.el.value);
        }
    }
}
FloatToInt.template = "float_to_int_field_widget.FloatToIntWidget"
FloatToInt.component = FloatToInt
FloatToInt.supportedTypes = ["float"]
registry.category("fields").add("float_to_int", {component: FloatToInt});