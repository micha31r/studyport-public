import * as app from '../../../../modules/app.js';

export default (function() {
    let sorted = {};

    for (let i=0; i<globalThis.rawData.length; i++) {
        let item = globalThis.rawData[i].fields;
        let subjectCode = item.subject.fields.subject_code;
        if (!(subjectCode in sorted)) {
            sorted[subjectCode] = [];
        }
        sorted[subjectCode].push({
            x: item.date,
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
        dom: "#line-chart1",
        data: data,
        options: {
            $x__type: "time",
            $y__callback: (value, index, values) => {
                let grade = app.conversion.numToResult(value);
                if (grade) {
                    return grade.toUpperCase();
                }
            },
            plugins: {
                htmlLegend: {}
            }
        }
    }).init();
});