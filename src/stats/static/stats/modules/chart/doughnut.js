/*
Usage:

let data = {
    labels: ["Jan", "Feb", "Mar", "Apr", "Mar", "Apr","Mar"],
    datasets: [{
        label: 'Number',
        data: [13,9,14,11,7,8,8],
        backgroundColor: app.themes.CHART_PALETTE,
        borderWidth: 2,
    }]
};

new app.chart.Doughnut({
    dom: "#doughnut-chart1",
    data: data,
}).init();
*/

import _chart from "./template.js";
import * as plugins from "./plugins/index.js";
import * as themes from "../themes.js";

export default class Doughnut extends _chart {
    static type = "doughnut";
    static options = {
        scales: {
            x: {
                display: false,
            },
            y: {
                display: false,
            },
        },
        plugins: {
            legend: {
                display: false,
            },
        }
    };
    static plugins = [plugins.legend.htmlLegendPlugin];
}