import * as app from '../../stats/modules/app.js';

export default (function(domSelector) {
    let sorted = {
        "success": 0,
        "fail": 0
    };

    globalThis.goalData.forEach(function(item, index) {
        sorted[item.fields.status]++;
    });

    let data = {
        labels: ["Success", "Fail"],
        datasets: [{
            data: Object.values(sorted),
            backgroundColor: [app.themes.getColor(0), app.themes.getColor(1)],
        }]
    };

    new app.chart.Doughnut({
        dom: domSelector,
        data: data,
    }).init();
});