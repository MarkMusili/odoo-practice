/** @odoo-module**/

import { Component } from "@odoo/owl";

export class DashboardItem extends Component{
    static template = "hospital_dashboard.DashboardItem";
    static props = {
        title: String,
        content: Number
    }
}
