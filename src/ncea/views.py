from django.utils import timezone
from django.conf import settings
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usermgmt.models import Student
from usermgmt.decorators import user_has_access
from settings.themes import get_theme
from standards.models import Subject, Assessment
from results.models import Result
from results.utils import get_results, calc_gpa
from results.conversion import abbv_to_name
from goal.models import Goal
from project import utils
from .certificate import has_certificate, get_certificate_endorsement, get_course_endorsement


@user_has_access
@login_required
def summary_view(request, level, **kwargs):
	ctx = {**kwargs}
	ctx = {**ctx, **get_theme(request.user)}

	try:
		level = int(level)
		if level not in [1,2,3]:
			raise Exception
	except:
		return redirect("ncea:summary", level=1)

	student = ctx["student"]
	results = get_results(student, include_empty=True)
	ctx["year_level"] = year_level = level + 10
	ctx["level"] = level

	if year_level > 10:
		ctx["year_gpas"] = {
			1: calc_gpa(get_results(student=student, assessment__level=1)),
			2: calc_gpa(get_results(student=student, assessment__level=2)),
			3: calc_gpa(get_results(student=student, assessment__level=3)),
		}

		passed, progress = has_certificate(student, year_level)
		ctx["passed"] = passed
		ctx["pass_progress"] = progress

		level, credits = get_certificate_endorsement(student, year_level)
		ctx["endorsement_level"] = abbv_to_name(level) if level else None
		ctx["endorsement_progress"] = {
			"a": credits["a"] + credits["m"] + credits["e"],
			"m": credits["m"] + credits["e"],
			"e": credits["e"],
		}

		ctx["subject_progress"] = subject_progress = {}
		for obj in student.get_subjects(year_level=year_level):
			_, credits = get_course_endorsement(student, obj.subject_code)
			a_sum = sum(credits["a"].values())
			m_sum = sum(credits["m"].values())
			e_sum = sum(credits["e"].values())

			subject_progress[obj.name] = {
				"pk": obj.pk,
				"progress": {
					"a": a_sum + m_sum + e_sum,
					"m": m_sum + e_sum,
					"e": e_sum,
				}
			}

		# Calculate credits gained in each year and NCEA level
		level_data = {}
		year_data = {}
		for obj in results.exclude(grade=None):
			if obj.assessment.level not in level_data:
				level_data[obj.assessment.level] = {
					"na": 0,
					"a": 0,
					"m": 0,
					"e": 0
				}
			if obj.date.year not in year_data:
				year_data[obj.date.year] = {
					"na": 0,
					"a": 0,
					"m": 0,
					"e": 0
				}
			level_data[obj.assessment.level][obj.grade] += obj.assessment.credits
			year_data[obj.date.year][obj.grade] += obj.assessment.credits

		ctx["level_data"] = level_data
		ctx["year_data"] = year_data
		ctx["student_data"] = utils.deep_serialize(student)
		ctx["raw_data"] = utils.deep_serialize(results.exclude(grade=None), max_depth=1)

	return render(request, "ncea/summary.html", ctx)



