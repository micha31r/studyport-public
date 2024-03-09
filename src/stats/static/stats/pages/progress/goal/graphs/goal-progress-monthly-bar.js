import * as app from '../../../../modules/app.js';

export default (function() {
    let sorted = {
        "success": new Array(12).fill(0),
        "fail": new Array(12).fill(0)
    };

    for (let i=0; i<globalThis.goalData.length; i++) {
        let item = globalThis.goalData[i].fields;
        if (item.end_date && item.repeat == "once") {
            let month;
            if (item.status == "success") {
                month = parseInt(item.completion_date.split("-")[1])-1
                sorted["success"][month] += 1;
            } else if (item.status == "fail") {
                month = parseInt(item.end_date.split("-")[1])-1
                sorted["fail"][month] -= 1;
            }
        }
    }

    let data = {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [
            {
                label: 'Failed',
                data: sorted["fail"],
                backgroundColor: app.themes.getColor(2),
            },
            {
                label: 'Successful',
                data: sorted["success"],
                backgroundColor: app.themes.getColor(1),
            },
        ]
    };

    new app.chart.Bar({
        dom: "#bar-chart2",
        data: data,
        options: {
            maxBarThickness: 10,
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false,
                    }
                },
            },
            $x__stacked: true,
            $y__stacked: true
        }
    }).init();
});