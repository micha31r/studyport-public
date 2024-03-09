/*
Usage:

let data = {
    labels: ["Jan", "Feb", "Mar", "Apr", "Mar", "Apr","Mar"],
    datasets: [{
        label: 'Number',
        data: [13,9,14,11,7,8,8],
        backgroundColor: app.themes.getColor(0),
        borderWidth: 0,
    }]
};

new app.chart.Bar({
    dom: "#bar-chart1",
    data: data,
}).init();
*/

import _chart from "./template.js";
import * as utils from "../utils.js";
import * as plugins from "./plugins/index.js";

export default class Bar extends _chart {
    static type = "bar";
    static options = {
        maxBarThickness: 40,
        plugins: {
            legend: {
                display: false,
            },
        }
    };
    static plugins = [plugins.legend.htmlLegendPlugin];
}