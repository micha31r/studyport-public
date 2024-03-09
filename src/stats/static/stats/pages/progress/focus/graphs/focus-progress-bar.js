import * as app from '../../../../modules/app.js';

export default (function() {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let sorted = {};
    let labels = [];

    for (let i=14; i>-1; i--) {
        let date = new Date();
        date.setDate(date.getDate() - (i-1));
        let key = date.toISOString().split('T')[0];
        key = monthNames[new Date(key).getMonth()] + " " + key.split("-")[2];
        sorted[key] = null;
        labels.push(key);
    }

    for (let i=0; i<globalThis.focusData.length; i++) {
        let item = globalThis.focusData[i].fields;
        let time = item.duration.split(":");
        let minutes = parseInt(time[0]) * 60 + parseInt(time[1]) + parseInt(time[2]) / 60;
        let date = monthNames[new Date(item.date).getMonth()] + " " + item.date.split("-")[2];
        sorted[date] += minutes;
    }

    let data = {
        labels: labels,
        datasets: [{
            label: 'Minutes',
            data: Object.values(sorted),
            backgroundColor: app.themes.getColor(1),
        }]
    };

    new app.chart.Bar({
        dom: "#bar-chart1",
        data: data,
        options: {
            maxBarThickness: 10,
        }
    }).init();
});