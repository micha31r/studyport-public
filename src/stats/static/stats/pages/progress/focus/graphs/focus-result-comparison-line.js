import * as app from '../../../../modules/app.js';

// Map value range to another range
// https://gist.github.com/xposedbones/75ebaef3c10060a3ee3b246166caab56
Number.prototype.map = function (in_min, in_max, out_min, out_max) {
  return (this - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

export default (function() {
    let focusData = []
    let resultData = [];
    let max = 0;

    for (let i=0; i<globalThis.focusData.length; i++) {
        let item = globalThis.focusData[i].fields;
        let time = item.duration.split(":");
        let minutes = parseInt(time[0]) * 60 + parseInt(time[1]) + parseInt(time[2]) / 60;
        if (new Date(item.date).getFullYear() == globalThis.student.fields.viewing_year) {
            focusData.push({
                x: new Date(item.date),
                y: minutes,
            });
            if (minutes > max) {
                max = minutes;
            }
        }
    }

    // Map values to between 0 - 3
    for (let i=0; i<focusData.length; i++) {
        focusData[i].y = focusData[i].y.map(0, max, 0, 3);
    }

    focusData.sort((a, b) => {
        return ((a.x < b.x) ? -1 : ((a.x > b.x) ? 1 : 0));
    });

    for (let i=0; i<globalThis.rawData.length; i++) {
        let item = globalThis.rawData[i].fields;
        if (item.grade) {
            resultData.push({
                x: new Date(item.date),
                y: app.conversion.gradeToNum(item.grade),
            });
        }
    }

    resultData.sort((a, b) => {
        return ((a.x < b.x) ? -1 : ((a.x > b.x) ? 1 : 0));
    });

    let data = {
        datasets: [
            {
                label: "Focus Minutes",
                data: focusData,
                pointBackgroundColor: app.themes.getColor(2),
                borderColor: app.themes.getColor(2),
                borderWidth: 2,
            },
            {
                label: "Grade",
                data: resultData,
                pointBackgroundColor: app.themes.getColor(1),
                borderColor: app.themes.getColor(1),
                borderWidth: 2,
            }
        ]
    };

    new app.chart.Line({
        dom: "#line-chart1",
        data: data,
        options: {
            $x__type: "time",
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    ticks: {
                        callback: (value, index, values) => {
                            return app.conversion.numToResult(value).toUpperCase();
                        }
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: {
                        // only want the grid lines for one axis to show up
                        drawOnChartArea: false,
                    },
                    ticks: {
                        callback: (value, index, values) => {
                            return parseInt(value.map(0, 1, 0, max));
                        }
                    }
                }
            }
        }
    }).init();
});