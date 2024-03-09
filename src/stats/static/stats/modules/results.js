import * as conversion from "./conversion.js";

function calcGPA(results) {
	let value = 0;
	let counter = 0;
	for (let i=0; i<results.length; i++) {
		let item = results[i].fields;
		let weighting = item.assessment.assessment_type == "i" ? item.student.fields.internal_weighting : item.student.fields.external_weighting;
		value += item.assessment.fields.credits + conversion.gradeToGPA(item.grade) * weighting;
		counter += item.assessment.fields.credits;
	}
	return value / (counter || 0);
}

function calcAvg(results) {
	let value = 0;
	let counter = 0;
	for (let i=0; i<results.length; i++) {
		let item = results[i].fields;
		let weighting = item.assessment.assessment_type == "i" ? item.student.fields.internal_weighting : item.student.fields.external_weighting;
		value += item.assessment.fields.credits + conversion.gradeToNum(item.grade) * weighting;
		counter += item.assessment.fields.credits;
	}
	return value / (counter || 0);
}

export {
	calcGPA,
	calcAvg,
}