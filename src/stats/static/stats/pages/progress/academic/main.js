import * as app from '../../../modules/app.js';
import subjectAverageGradeBar from './graphs/subject-average-grade-bar.js';
import subjectAssessmentGradeLine from './graphs/subject-assessment-grade-line.js';
import subjectCreditsBar from './graphs/subject-credits-bar.js';

window.addEventListener("load", function() {
    globalThis.rawData = app.data.getDomData("#raw-data");
    globalThis.student = app.data.getDomData("#student-data");
    app.config.AppConfig.gradingSystem = globalThis.student.fields.grading_system;

    subjectCreditsBar();
    subjectAssessmentGradeLine();
    subjectAverageGradeBar();
});