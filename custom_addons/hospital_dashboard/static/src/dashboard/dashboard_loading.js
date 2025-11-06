/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";

export class DashboardLoader extends Component {
    static components = { LazyComponent };
    static template = xml`
        <LazyComponent bundle="'hospital_dashboard.dashboard'" Component="'HospitalDashboard'" />
    `;
}

registry.category("actions").add("hospital_dashboard.HospitalDashboard", DashboardLoader);