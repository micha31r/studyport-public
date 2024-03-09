import * as app from '../../../../modules/app.js';

export default (function() {
    let ongoing = 0;
    let fail = 0;
    let success = 0;

    for (let i=0; i<globalThis.goalData.length; i++) {
        let item = globalThis.goalData[i].fields;
        if (item.repeat == "once") {
            switch (item.status) {
                case "ongoing":
                    ongoing += 1;
                    break;
                case "fail":
                    fail += 1;
                    break;
                case "success":
                    success += 1;
                    break;
            }
        }
    }

    let data = {
        labels: ["Failed", "Ongoing", "Successful"],
        datasets: [{
                label: 'Failed',
                data: [fail, ongoing, success],
                backgroundColor: [app.themes.getColor(2), app.themes.getColor(0), app.themes.getColor(1)],
        }]
    };

    new app.chart.Doughnut({
        dom: "#doughnut-chart1",
        data: data,
    }).init();
});