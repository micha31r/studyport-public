from results.models import Result
from results.utils import get_results

# Credits from the current year level required to for a certificate
CREDITS_REQUIRED = {
	11: 80,
	12: 60,
	13: 60,
}

TOTAL_REQUIRED = 80

COURSE_ENDORSEMENT_EXCEPTIONS = {
	"Physical Education1",
	"Physical Education2",
	"Physical Education3",
	"Religious Studies1",
	"Religious Studies2",
	"Religious Studies3",
	"Visual Arts3"
}

# NCEA certificate
def has_certificate(student, _year_level=None):
	year_level = _year_level or student.year_level
	
	qs = get_results(
		student,
		date__year__lte = student.to_year(year_level),
	).exclude(grade="na")

	credits = {
		11:0,
		12:0,
		13:0,
		# Just here to prevent key error
		14:0,
		15:0,
	}
	for obj in qs:
		credits[obj.assessment.get_year_level()] += obj.assessment.credits

	total = sum(credits.values())
	extra = 0
	
	if year_level == 11:
		if total < TOTAL_REQUIRED:
			extra = TOTAL_REQUIRED - total
	elif year_level == 12:
		if credits[12] + credits[13] < CREDITS_REQUIRED[12]:
			extra += CREDITS_REQUIRED[12] - (credits[12] + credits[13])
		if total - CREDITS_REQUIRED[12] < TOTAL_REQUIRED - CREDITS_REQUIRED[12]:
			extra += TOTAL_REQUIRED - CREDITS_REQUIRED[12] - (total - CREDITS_REQUIRED[12])
	elif year_level == 13:
		if credits[13] < CREDITS_REQUIRED[13]:
			extra += CREDITS_REQUIRED[13] - credits[13]
		if total - CREDITS_REQUIRED[13] < TOTAL_REQUIRED - CREDITS_REQUIRED[13]:
			extra += TOTAL_REQUIRED - CREDITS_REQUIRED[13] - (total - CREDITS_REQUIRED[13])
		
	if extra > 80:
		extra = 80

	return False if extra else True, extra


# NCEA certificate endorsement
def get_certificate_endorsement(student, _year_level=None):
	year_level = _year_level or student.year_level

	qs = get_results(
		student,
		assessment__level__gte = year_level - 10,
		date__year__lte = student.to_year(year_level),
	).exclude(grade="na")

	credits = {
		"a":0,
		"m":0,
		"e":0,
	}
	for obj in qs:
		if obj.grade not in credits:
			credits[obj.grade] = 0
		credits[obj.grade] += obj.assessment.credits

	level = None

	if credits["e"] >= 50:
		level = "e"
	elif credits["m"] + credits["e"] >= 50:
		level = "m"
	elif credits["a"] + credits["m"] + credits["e"] >= 50:
		level = "a"

	return level, credits


# Get endorsement data for a subject
def get_course_endorsement(student, subject_code):

	qs = get_results(
		student,
		subject__subject_code = subject_code,
	).exclude(grade="na")

	credits = {
		"a": {"i":0,"e":0},
		"m": {"i":0,"e":0},
		"e": {"i":0,"e":0},
	}
	for obj in qs:
		if obj.grade:
			credits[obj.grade][obj.assessment.assessment_type] += obj.assessment.credits

	level = None
	a_sum = sum(credits["a"].values())
	m_sum = sum(credits["m"].values())
	e_sum = sum(credits["e"].values())

	if e_sum >= 14 and \
		(subject_code in COURSE_ENDORSEMENT_EXCEPTIONS or \
			(credits["e"]["i"] >= 3 and \
				credits["e"]["e"] >= 3)):
		level = "e"
	elif m_sum + e_sum >= 14 and \
		(subject_code in COURSE_ENDORSEMENT_EXCEPTIONS or \
			(credits["m"]["i"] + credits["e"]["i"] >= 3 and \
				credits["m"]["e"] + credits["e"]["e"] >= 3)):
		level = "m"
	elif a_sum + m_sum + e_sum >= 14 and \
		(subject_code in COURSE_ENDORSEMENT_EXCEPTIONS or \
			(credits["a"]["i"] + credits["m"]["i"] + credits["e"]["i"] >= 3 and \
				credits["a"]["e"] + credits["m"]["e"] + credits["e"]["e"] >= 3)):
		level = "a"

	return [level, credits]


# Get endorsement data for every subject
def get_all_course_endorsements(student, _year_level=None):
	year_level = _year_level or student.year_level

	qs = get_results(
		student,
		assessment__level = year_level - 10,
	).exclude(grade="na")

	courses = {}
	for obj in qs:
		if obj.grade:
			if obj.subject.subject_code not in courses:
				courses[obj.subject.subject_code] = {
					"a": {"i":0,"e":0},
					"m": {"i":0,"e":0},
					"e": {"i":0,"e":0},
				}
			courses[obj.subject.subject_code][obj.grade][obj.assessment.assessment_type] += obj.assessment.credits

	endorsements = {}
	for subject_code, credits in courses.items():
		level = None
		a_sum = sum(credits["a"].values())
		m_sum = sum(credits["m"].values())
		e_sum = sum(credits["e"].values())

		if e_sum >= 14 and \
			(subject_code in COURSE_ENDORSEMENT_EXCEPTIONS or \
				(credits["e"]["i"] >= 3 and \
					credits["e"]["e"] >= 3)):
			level = "e"
		elif m_sum + e_sum >= 14 and \
			(subject_code in COURSE_ENDORSEMENT_EXCEPTIONS or \
				(credits["m"]["i"] + credits["e"]["i"] >= 3 and \
					credits["m"]["e"] + credits["e"]["e"] >= 3)):
			level = "m"
		elif a_sum + m_sum + e_sum >= 14 and \
			(subject_code in COURSE_ENDORSEMENT_EXCEPTIONS or \
				(credits["a"]["i"] + credits["m"]["i"] + credits["e"]["i"] >= 3 and \
					credits["a"]["e"] + credits["m"]["e"] + credits["e"]["e"] >= 3)):
			level = "a"

		endorsements[subject_code] = [level, credits]

	return endorsements






