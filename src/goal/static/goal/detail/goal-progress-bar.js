import * as app from '../../stats/modules/app.js';

export default (function(dom) {
    let sorted = new Array(14);
    let startingCycle = globalThis.goalData[0].fields.cycle;
    let labelPrefix = globalThis.goalData[0].fields.goal.fields.repeat[0];

    globalThis.goalData.forEach(function(item, index) {
        sorted[index] = item.fields.value;
    });

    let data = {
        labels: [...Array(14).keys()].map(x => labelPrefix + (startingCycle + x + 1)),
        datasets: [{
            data: sorted,
            backgroundColor: app.themes.getColor(1),
        }]
    };

    new app.chart.Bar({
        dom: dom,
        data: data,
        options: {
            maxBarThickness: 10,
        }
    }).init();
});