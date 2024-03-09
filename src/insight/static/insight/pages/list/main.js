import * as app from '../../../stats/modules/app.js';
import subjectAssessmentGradeLine from './subject-assessment-grade-line.js';

window.addEventListener("load", function() {
    globalThis.rawData = app.data.getDomData("#raw-data");
    globalThis.student = app.data.getDomData("#student-data");
    app.config.AppConfig.gradingSystem = globalThis.student.fields.grading_system;

    let sorted = {};
    for (let i=0; i<globalThis.rawData.length; i++) {
        let item = globalThis.rawData[i].fields;
        let subjectCode = item.subject.fields.subject_code;
        if (!(subjectCode in sorted)) {
            sorted[subjectCode] = [];
        }
        sorted[subjectCode].push(globalThis.rawData[i]);
    }
    
    let keys = Object.keys(sorted);
    for (let i=0; i<keys.length; i++) {
        subjectAssessmentGradeLine("#line-chart-"+keys[i], sorted[keys[i]]);
    }
});