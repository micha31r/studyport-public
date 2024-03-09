import * as app from '../../../modules/app.js';

export default (function(domSelector) {
    let sorted = {};

    // Doughnut chart
    for (let i=0; i<globalThis.rawData.length; i++) {
        let item = globalThis.rawData[i].fields;
        if (item.grade in sorted) {
            sorted[item.grade] += item.assessment.fields.credits;
        } else {
            sorted[item.grade] = item.assessment.fields.credits;
        }
    }

    let labels = Object.keys(sorted);
    let data = {
        labels: labels,
        datasets: [{
            label: 'Number',
            data: Object.values(sorted),
            backgroundColor: [
                app.themes.assignColor(labels[0]),
                app.themes.assignColor(labels[1]),
                app.themes.assignColor(labels[2])
            ],
            borderWidth: 2,
        }]
    };

    new app.chart.Doughnut({
        dom: domSelector,
        data: data,
        options: {
            cutout: "40%",
        }
    }).init();
});