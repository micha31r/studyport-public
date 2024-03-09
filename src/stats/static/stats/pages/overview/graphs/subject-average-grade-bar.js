import * as app from '../../../modules/app.js';

export default (function() {
	let sorted = {};

    for (let i=0; i<globalThis.rawData.length; i++) {
        let item = globalThis.rawData[i].fields;
        let code = item.subject.fields.subject_code;
        if (!(code in sorted)) {
            sorted[code] = [];
        }
        sorted[code].push(globalThis.rawData[i])
    }

    let avg = {};
    for (let [k, v] of Object.entries(sorted)) {
        avg[k] = app.results.calcGPA(v);
    }

    let data = {
        labels: Object.keys(avg),
        datasets: [{
            label: 'Average',
            data: Object.values(avg),
            backgroundColor: app.themes.CHART_PALETTE,
        }]
    };

    new app.chart.Bar({
        dom: "#bar-chart1",
        data: data,
    }).init();
});