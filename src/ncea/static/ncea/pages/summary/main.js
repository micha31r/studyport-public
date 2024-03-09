import * as app from '../../../stats/modules/app.js';
import assessmentGradeLine from './assessment-grade-line.js';
import NCEALevelCreditsBar from './ncea-level-credits-bar.js';

window.addEventListener("load", function() {
    globalThis.rawData = app.data.getDomData("#raw-data");
    globalThis.student = app.data.getDomData("#student-data");
    app.config.AppConfig.gradingSystem = globalThis.student.fields.grading_system;

    NCEALevelCreditsBar("#bar-chart-1");
    assessmentGradeLine("#line-chart-1");
});