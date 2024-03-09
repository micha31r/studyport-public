import * as config from "./config.js";
import * as utils from "./utils.js";


const GRADING_SYSTEMS = {
	"ncea": {
		"na": 0,
		"a": 1,
		"m": 2,
		"e": 3,
	},
	"alphabetical": {
		"f": 0,
		"d-": 0.5,
		"d": 1,
		"d+": 1.5,
		"c-": 2,
		"c": 2.5,
		"c+": 3,
		"b-": 3.5,
		"b": 4,
		"b+": 4.5,
		"a-": 5,
		"a": 5.5,
		"a+": 6,
	}
};

const GPA_SCALE = {
	"ncea": {
		"na": 0,
		"a": 2,
		"m": 3,
		"e": 4,
	},
	"alphabetical": {
		"f": 0,
		"d-": 0.7,
		"d": 1,
		"d+": 1.3,
		"c-": 1.7,
		"c": 2,
		"c+": 2.3,
		"b-": 2.7,
		"b": 3,
		"b+": 3.3,
		"a-": 3.7,
		"a": 4,
		"a+": 4.3,
	}
}

// Convert grade string to number
function gradeToNum(grade) {
	grade = grade.toLowerCase();
	try {
		return GRADING_SYSTEMS[config.AppConfig.gradingSystem][grade];
	} catch (err) {
		return null;
	}
}

// Convert grade string to GPA number
function gradeToGPA(grade) {
	grade = grade.toLowerCase();
	try {
		return GPA_SCALE[config.AppConfig.gradingSystem][grade];
	} catch (err) {
		return null;
	}
}

// Retrieve grade number based on index
function indexToResult(index) {
	qs = config.AppConfig.gradingSystem;
	let keys = Object.keys(GRADING_SYSTEMS[gs]);
	return GRADING_SYSTEMS[gs][keys[index]];
}

// Convert grade number to string
function numToResult(number) {
	try {
		for (let [k, v] of Object.entries(GRADING_SYSTEMS[config.AppConfig.gradingSystem])) {
			if (number == v) {
				return k;
			}
		}
		return null;
	} catch (err) {
		return null;
	}
}

// Check that grade is valid for a given grading system
function gradeIsValid(grade) {
	grade = grade.toLowerCase();
	if (grade != "undefined" && grade in GRADING_SYSTEMS[config.AppConfig.gradingSystem]) {
		return true;
	}
	return false;
}

export {
	GRADING_SYSTEMS,
	GPA_SCALE,
	gradeToNum,
	gradeToGPA,
	indexToResult,
	numToResult,
	gradeIsValid,
}

