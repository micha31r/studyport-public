/*
Usage:

let data = {
    labels: ["Jan", "Feb", "Mar", "Apr", "Mar", "Apr","Mar"],
    datasets: [{
        label: 'Number',
        data: [13,9,14,11,7,8,8],
        pointBackgroundColor: app.themes.getColor(0),
        borderColor: app.themes.getColor(0),
        borderWidth: 2,
    }]
};

new app.chart.Line({
    dom: "#line-chart1",
    data: data,
    options: {
        fill: true,
        $gradientBackground: 0,
    },
}).init();
*/

import _chart from "./template.js";
import * as plugins from "./plugins/index.js";
import * as themes from "../themes.js";

export default class Line extends _chart {
    static type = "line";
    static options = {
        plugins: {
            gradient: false,
            legend: {
                display: false,
            },
        },
    };
    static plugins = [
        plugins.gradient.gradientBackgroundPlugin,
        plugins.legend.htmlLegendPlugin
    ];
}