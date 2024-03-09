import * as app from '../../../stats/modules/app.js';

export default (function(domSelector) {
    let sorted = {};

    for (let i=0; i<globalThis.rawData.length; i++) {
        let item = globalThis.rawData[i].fields;
        let year = item.date.split("-")[0];

        if (!(year in sorted)) {
            sorted[year] = [];
        }

        let date = new Date(item.date)
        date.setYear(0)
        sorted[year].push({
            x: date,
            y: app.conversion.gradeToNum(item.grade),
        });
    }

    for (let [k, v] of Object.entries(sorted)) {
        sorted[k].sort((a, b) => {
            return ((a.x < b.x) ? -1 : ((a.x > b.x) ? 1 : 0));
        });
    }

    let counter = -1;
    let data = {
        datasets: Object.entries(sorted).map(item => {
            counter++;
            let key = item[0];
            let value = item[1];
            return {
                label: key,
                data: value,
                pointBackgroundColor: app.themes.getColor(counter),
                borderColor: app.themes.getColor(counter),
                borderWidth: 2,
            }
        })
    };

    new app.chart.Line({
        dom: domSelector,
        data: data,
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        title: (context) => {
                            let date = new Date(context[0].dataset.data[context[0].dataIndex].x);
                            return date.toLocaleString('en-nz',{month:'short', day:"numeric"});
                        },
                        label: (context) => {
                            return app.conversion.numToResult(context.dataset.data[context.dataIndex].y).toUpperCase();
                        },
                        afterLabel: (context) => {
                            return "Year " + context.dataset.label;
                        }
                    }
                },
                htmlLegend: {},
            },
            $x__type: "time",
            $y__callback: (value, index, values) => {
                let grade = app.conversion.numToResult(value);
                if (grade) {
                    return grade.toUpperCase();
                }
            },
        }
    }).init();
});