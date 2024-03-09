import * as app from '../../../modules/app.js';
import goalProgressDoughnut from './graphs/goal-progress-doughnut.js';
import goalProgressMonthlyBar from './graphs/goal-progress-monthly-bar.js';
// import performanceBar from './graphs/performance-bar.js';


function calcEarlyCompletion() {
    let over = 0;
    let overCounter = 0;

    for (let i=0; i<globalThis.goalData.length; i++) {
        let item = globalThis.goalData[i].fields;
        if (item.repeat == "once" && item.status == "success" && item.completion_date && item.end_date && item.end_option == "before") {
            // Calculate the interval between completion date and the deadline
            let dayInterval = (new Date(item.end_date) - new Date(item.completion_date)) / 60 / 60 / 24 / 1000;
            over += dayInterval;
            overCounter++;
        }
    }

    return (over / overCounter).toFixed(2);
}

function setPerformanceProgressBars() {
    let under = 0;
    let underCounter = 0;
    let over = 0;
    let overCounter = 0;

    for (let i=0; i<globalThis.goalData.length; i++) {
        let item = globalThis.goalData[i].fields;
        if (item.end_date && item.repeat == "once") {
            if (item.status == "success") {
                over += (item.current / item.target - 1) * 100;
                overCounter++;
            } else if (item.status == "fail") {
                under += (1 - item.current / item.target) * 100;
                underCounter++;
            }
        }
    }

    under /= underCounter;
    over /= overCounter;

    document.querySelector("#under-bar").style.width = under + "%";
    document.querySelector("#over-bar").style.width = over + "%";
}


window.addEventListener("load", function() {
    globalThis.goalData = app.data.getDomData("#goal-data");
    globalThis.student = app.data.getDomData("#student-data");
    app.config.AppConfig.gradingSystem = globalThis.student.fields.grading_system;

    goalProgressDoughnut();
    goalProgressMonthlyBar();
    setPerformanceProgressBars();

    document.querySelector(".early-completion .amount").innerText = calcEarlyCompletion();
});