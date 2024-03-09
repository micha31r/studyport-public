GRADING_SYSTEMS = {
	"ncea": {
		"na": 1,
		"a": 2,
		"m": 3,
		"e": 4,
	},
	"alphabetical": {
		"f": 0.5,
		"d-": 1,
		"d": 1.5,
		"d+": 2,
		"c-": 2.5,
		"c": 3,
		"c+": 3.5,
		"b-": 4,
		"b": 4.5,
		"b+": 5,
		"a-": 5.5,
		"a": 6,
		"a+": 6.5,
	}
}

GPA_SCALE = {
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

NAME_TO_ABBV = {
	"not achieved": "na",
	"achieved": "a",
	"merit": "m",
	"excellence": "e",

	# Some school results begins with "achieved with"
	"achieved with merit": "m",
	"achieved with excellence": "e",
}

ABBV_TO_NAME = {
	"na": "not achieved",
	"a": "achieved",
	"m": "merit",
	"e": "excellence",
}


# Convert name to abbreviation
def name_to_abbv(string):
	s = string.lower()
	if s in NAME_TO_ABBV:
		return NAME_TO_ABBV[s]
	return None


# For NCEA only
# Convert from abbreviation to name
def abbv_to_name(string):
	s = string.lower()
	if s in ABBV_TO_NAME:
		return ABBV_TO_NAME[s]
	return None


# Convert grade to number
def grade_to_num(gs, grade):
	try:
		return GRADING_SYSTEMS[gs.lower()][grade.lower()]
	except:
		return None


# Convert grade to GPA number
def grade_to_GPA(gs, grade):
	try:
		return GPA_SCALE[gs.lower()][grade.lower()]
	except:
		return None


# Check that the grade is valid for a given grading system
def grade_is_valid(gs, grade):
	grade = grade.lower()
	if grade and grade in GRADING_SYSTEMS[gs.lower()]:
		return True
	return False

