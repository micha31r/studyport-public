import * as themes from "../../themes.js";

function setGradient(chart, colorIndex) {
    let rgb = themes.hexToRGB(themes.CHART_PALETTE[colorIndex]);
    
    if (chart.chartArea) {
        let gradient = chart.ctx.createLinearGradient(0, chart.chartArea.top, 0, chart.chartArea.bottom);
        gradient.addColorStop(0, `rgb(${rgb.r},${rgb.g},${rgb.b},0.5)`);   
        gradient.addColorStop(1, `rgb(${rgb.r},${rgb.g},${rgb.b},0)`);
        chart.data.datasets.forEach(x => {x.backgroundColor = gradient});
    }
}

// Plugin events map
// https://www.chartjs.org/docs/3.7.0/developers/plugins.html

export const gradientBackgroundPlugin = {
    id: "gradient",
    beforeInit: (chart, args, options) => {
        // resize event is not called if chart is not responsive
        if (chart._options.responsive == false) {
            chart.update();
            setGradient(chart, options.colorIndex);
            // chart will be updated automatically as shown
            // in the process flow chart
        }
    },
    resize: (chart, args, options) => {
        // Must update chart first to force a render cycle because
        // chart.chartArea is only updated after first render
        chart.update();
        setGradient(chart, options.colorIndex);
        // Update again to render the new gradient
        chart.update();
    },
}