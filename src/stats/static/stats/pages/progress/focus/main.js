import * as app from '../../../modules/app.js';
import focusProgressBar from './graphs/focus-progress-bar.js';
import focusResultComparisonLine from './graphs/focus-result-comparison-line.js';

window.addEventListener("load", function() {
    globalThis.focusData = app.data.getDomData("#focus-data");
    globalThis.rawData = app.data.getDomData("#raw-data");
    globalThis.student = app.data.getDomData("#student-data");
    app.config.AppConfig.gradingSystem = globalThis.student.fields.grading_system;

    focusProgressBar();
    focusResultComparisonLine();
});