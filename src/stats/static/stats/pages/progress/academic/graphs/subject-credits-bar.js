import * as app from '../../../../modules/app.js';

export default (function() {
	let sorted = {};

    for (let i=0; i<globalThis.rawData.length; i++) {
        let item = globalThis.rawData[i].fields;
        let code = item.subject.fields.subject_code;
        if (!(code in sorted)) {
            sorted[code] = [];
        }
        sorted[code].push(globalThis.rawData[i])
    }

    let levels = {};
    let subjectCodes = Object.keys(sorted);
    for (let [k, v] of Object.entries(sorted)) {
        for (let i=0; i<v.length; i++) {
            let item = v[i].fields;
            if (!(item.grade in levels)) {
                levels[item.grade] = {};
                for (let s=0; s<subjectCodes.length; s++) {
                    levels[item.grade][subjectCodes[s]] = 0;
                }
            }
            levels[item.grade][item.subject.fields.subject_code] += item.assessment.fields.credits;
        }
    }

    let data = {
        labels: subjectCodes,
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
        dom: "#bar-chart2",
        data: data,
        options: {
            $x__stacked: true,
            $y__stacked: true,
        }
    }).init();
});