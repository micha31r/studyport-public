import * as app from '../../../stats/modules/app.js';

export default (function(domSelector, rawData) {
    let sorted = [];

    for (let i=0; i<rawData.length; i++) {
        let item = rawData[i].fields;
        sorted.push({
            x: item.date,
            y: app.conversion.gradeToNum(item.grade),
        });
    }
    
    sorted.sort((a, b) => {
        return ((a.x < b.x) ? -1 : ((a.x > b.x) ? 1 : 0));
    });

    let data = {
        datasets: [{
            label: 'Average grade',
            data: sorted,
            pointRadius: 0,
            borderColor: app.themes.getColor(0),
            borderWidth: 2,
        }]
    };

    new app.chart.Line({
        dom: domSelector,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    display: false,
                },
                y: {
                    display: false,
                },
            },
            fill: true,
            $gradient: 0,
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