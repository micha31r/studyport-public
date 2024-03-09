import * as app from '../../stats/modules/app.js';
import goalProgressBar from './goal-progress-bar.js';
import overviewDoughnut from './overview-doughnut.js';

window.addEventListener("load", function() {
    globalThis.goalData = app.data.getDomData("#goal-data");
    globalThis.rawData = app.data.getDomData("#raw-data");
    globalThis.student = app.data.getDomData("#student-data");
    app.config.AppConfig.gradingSystem = globalThis.student.fields.grading_system;

    goalProgressBar("#bar-chart1");
    overviewDoughnut("#doughnut-chart1");
});