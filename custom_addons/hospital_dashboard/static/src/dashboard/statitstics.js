/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const loadPatientData = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const statistics = reactive({});

        async function loadData() {
            console.log("Fetching data...");
            const data = await rpc('/hospital_dashboard/data');
            Object.assign(statistics, data);
            console.log(data);
        }

        loadData();

        return statistics;
    }
}

registry.category("services").add("loadPatientData", loadPatientData);