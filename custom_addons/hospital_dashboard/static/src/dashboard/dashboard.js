/** @odoo-module **/

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";



export class HospitalDashboard extends Component {
    static template = "hospital_dashboard.HospitalDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup () {
        this.display = {
            controlPanel: {}
        };
        this.statistics = useService("loadPatientData");
    }
}

registry.category("lazy_components").add("HospitalDashboard", HospitalDashboard);
