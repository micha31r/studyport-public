import * as app from '../../modules/app.js';
import calcRankScore from './rank-score.js';
import assessmentGradeLine from './graphs/assessment-grade-line.js';
import creditsDoughnut from './graphs/credits-doughnut.js';
import subjectAverageGradeBar from './graphs/subject-average-grade-bar.js';

window.addEventListener("load", function() {
    globalThis.rawData = app.data.getDomData("#raw-data");
    globalThis.student = app.data.getDomData("#student-data");
    app.config.AppConfig.gradingSystem = globalThis.student.fields.grading_system;

    let rankScoreData = app.data.getDomData("#rank-score-data");
    document.querySelector("#rank-score").innerText = (rankScoreData.length > 0 ? calcRankScore(rankScoreData) : "--");
    assessmentGradeLine("#line-chart1");
    creditsDoughnut("#doughnut-chart1");
});