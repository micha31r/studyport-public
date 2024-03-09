from playground.models import Playground
from .models import Result
from .conversion import grade_to_num, grade_to_GPA, name_to_abbv, grade_is_valid

def get_results(student, include_empty=False, ignore_visibility=False, **kwargs):
	qs = Result.objects.filter(
		student = student,
		**kwargs,
	)

	if not ignore_visibility:
		qs = qs.filter(is_published=True)
		if not student.show_mock_results:
			qs = qs.exclude(is_mock=True)

	# Filter playground aliases
	if student.recent_playground_id:
		playground, _ = Playground.objects.get_or_create(pk=student.recent_playground_id, student=student)
		source_ids = playground.get_source_ids() if student.playground_is_active else playground.get_result_ids()
		qs = qs.exclude(pk__in=source_ids)

	if not include_empty:
		qs = qs.exclude(grade=None)
	return qs


"""
Year passing rules:
Level 1: gain 80 credits ar level 1 or above
Level 2: gain 60 credits at level 2 or above + 20 credits at level 1 or above
Level 3: gain 60 credits at level 3 or above + 20 credits at level 2 or above
"""

# Arg 'grades' is all grades
# Arg 'current_level' is the student's current year level
def year_passed(grades, current_level):
	credits = {
		"Year 11": 0,
		"Year 12": 0,
		"Year 13": 0,
	}

	for item in grades:
		sub_levels = []
		abbv = name_to_abbv(item.grade)
		if abbv != "na":
			if item.year_level <= 11: # Include accelerant students
				sub_levels.append("Year 11")
			elif item.year_level == 12:
				sub_levels.append("Year 11")
				sub_levels.append("Year 12")
			elif item.year_level == 13:
				sub_levels.append("Year 11")
				sub_levels.append("Year 12")
				sub_levels.append("Year 13")
			for level in sub_levels:
				credits[level] += item.credits

	# Check if the student has passed
	# Set to true if endorsed otherwise return the number of credits needed
	passed = None
	primary_level = "Year 11" # 60 credits
	secondary_level = "Year 11" # 20 credits
	if current_level == 4:
		# Year 12: 60 level 2 + 20 level 1
		primary_level = "Year 12"
	elif current_level == 5:
		# Year 13: 60 level 3 + 20 level 2
		primary_level = "Year 13"
		secondary_level = "Year 12"

	primary_level_credits_required = 80 - min(credits[secondary_level], 20)
	
	if credits[primary_level] < primary_level_credits_required:
		passed = primary_level_credits_required - credits[primary_level]
	else:
		passed = True
	return passed


"""
Year endorsement rules:
At least 50 credits in level Achieved, Merit, or Excellence
"""

# Arg 'grades' is all grades
def year_endorsed(grades, current_level):
	credits = {
		"a": 0,
		"m": 0,
		"e": 0,
	}

	for item in grades:
		if item.year_level >= current_level:
			sub_levels = []
			abbv = name_to_abbv(item.grade)
			if abbv != "na":
				if abbv == "a":
					sub_levels.append("a")
				elif abbv == "m":
					sub_levels.append("a")
					sub_levels.append("m")
				elif abbv == "e":
					sub_levels.append("a")
					sub_levels.append("m")
					sub_levels.append("e")
				for level in sub_levels:
					credits[level] += item.credits

	# Check for endorsement
	# Set to true if endorsed otherwise return the current number of credits
	endorsement = {
		"a": None,
		"m": None,
		"e": None,
	}

	for level, number in credits.items():
		if number < 50:
			endorsement[level] = number
		else:
			endorsement[level] = True
	return endorsement


"""
Course endorsement rules:
At least 14 credits in level Achieved, Merit, or Excellence
At least three of them must be externally assessed and three of them internally assessed
The 2nd rule does not apply to Physical Education, Religious Studies and level 3 Visual Arts
"""

ENDORSEMENT_EXCEPTIONS = [
	{
		"name": "Physical Education",
		"levels": [11,12,13],
	},
	{
		"name": "Religious Studies",
		"levels": [11,12,13],
	},
	{
		"name": "Visual Arts",
		"levels": [13],
	},
]

# Check whether the student has endorsed a subject, if not, then return the current number of credits
# Arg 'grades' is all grades in a specific subject
def course_endorsed(grades):
	use_exception = False
	for exception in ENDORSEMENT_EXCEPTIONS:
		if grades[0].subject_name == exception["name"] and grades[0].year_level in exception["levels"]:
			use_exception = True

	# Calculate accumulative credits
	# Excellence credits will be added to e, m and a
	# Merit credits will be added to m and a
	# Achieved credits will only be added to a

	credits = {
		"a": {"internal":0, "external":0},
		"m": {"internal":0, "external":0},
		"e": {"internal":0, "external":0},
	}

	for item in grades:
		sub_levels = []
		abbv = name_to_abbv(item.grade)
		if abbv != "na":
			if abbv == "a":
				sub_levels.append("a")
			elif abbv == "m":
				sub_levels.append("a")
				sub_levels.append("m")
			elif abbv == "e":
				sub_levels.append("a")
				sub_levels.append("m")
				sub_levels.append("e")
			for level in sub_levels:
				if item.assessment.assessment_type == "external": 
					credits[level]["external"] += item.credits
				else:
					credits[level]["internal"] += item.credits

	# Check for endorsement
	# Set to true if endorsed otherwise return the current number of credits
	endorsement = {
		"a": {},
		"m": {},
		"e": {},
	}

	for level, item in credits.items():
		met_requirements = True
		if item["internal"] + item["external"] < 14 or not use_exception and (item["external"] < 3 or item["internal"] < 3):
			met_requirements = False
		if not met_requirements:
			endorsement[level]["internal"] = item["internal"]
			endorsement[level]["external"] = item["external"]
		else:
			endorsement[level] = True
	return endorsement
	

def calc_gpa(qs):
	value = 0
	counter = 0
	for obj in qs:
		value += obj.assessment.credits * grade_to_GPA(obj.student.grading_system, obj.grade) * obj.student.get_weighting(obj.assessment.assessment_type)
		counter += obj.assessment.credits
	return value / (counter or 1)






