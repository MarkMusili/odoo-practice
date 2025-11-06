/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "hospital_dashboard.PieChart";
    static props = {
        data: Object
    }

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));

        onMounted(() => this.renderChart());

    }
    renderChart() {
        new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        label: "Patients by Gender",
                        data: Object.values(this.props.data),
                    },
                ],
            }
        });
    }

}