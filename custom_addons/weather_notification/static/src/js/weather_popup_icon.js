/** odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart,useState} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';


class WeatherPopup extends Component {
    setup() {
        this.dialog = useService('dialog');
        this.orm = useService('orm');
        this.state = useState({ weatherData: false });
        onWillStart(async () => {
            const weatherData = await this.orm.call('weather.content','get_weather_content',[]);
            this.state.weatherData = weatherData;
        });
    }
}
WeatherPopup.template = "weather_popup_icon";
WeatherPopup.components = {
     Dropdown,
    DropdownItem,
};

export const WeatherPopupItem = {
    Component: WeatherPopup
};
registry.category("systray").add(
    "WeatherPopup",
    WeatherPopupItem,
    { sequence: 2 }

);



