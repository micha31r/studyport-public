import * as app from '../../../stats/modules/app.js';

export default (function(domSelector) {
	let sorted = {
        1: [],
        2: [],
        3: [],
    };

    for (let i=0; i<globalThis.rawData.length; i++) {
        let item = globalThis.rawData[i].fields;
        let level = item.assessment.fields.level;
        if (!(level in sorted)) {
            sorted[level] = [];
        }
        sorted[level].push(globalThis.rawData[i])
    }

    let levels = {};
    let nceaLevels = Object.keys(sorted);
    for (let [k, v] of Object.entries(sorted)) {
        for (let i=0; i<v.length; i++) {
            let item = v[i].fields;
            if (!(item.grade in levels)) {
                levels[item.grade] = {};
                for (let s=0; s<nceaLevels.length; s++) {
                    levels[item.grade][nceaLevels[s]] = 0;
                }
            }
            levels[item.grade][item.assessment.fields.level] += item.assessment.fields.credits;
        }
    }

    let data = {
        labels: nceaLevels,
        datasets: Object.entries(levels).map(item => {
            let key = item[0];
            let value = item[1];
            return {
                label: key,
                data: Object.values(value),
                backgroundColor: app.themes.assignColor(key),
            }
        })
    };

    new app.chart.Bar({
        dom: domSelector,
        data: data,
        options: {
            scales: {
                x: {
                    ticks: {
                        callback: (value, index, values) => {
                            return "Level " + (value + 1);
                        },
                    },
                },
            },
            $x__stacked: true,
            $y__stacked: true,
        }
    }).init();
});