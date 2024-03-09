import * as app from '../../../stats/modules/app.js';
import assessmentGradeLine from '../../../stats/pages/overview/graphs/assessment-grade-line.js';
import creditsDoughnut from '../../../stats/pages/overview/graphs/credits-doughnut.js';

window.addEventListener("load", function() {
    globalThis.rawData = app.data.getDomData("#raw-data");
    globalThis.student = app.data.getDomData("#student-data");
    app.config.AppConfig.gradingSystem = globalThis.student.fields.grading_system;

    assessmentGradeLine("#line-chart-1");
    creditsDoughnut("#doughnut-chart-1");
});