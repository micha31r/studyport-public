import demjson3
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
from results.utils import get_results
from goal.models import Goal
from stats.utils import get_subject_gpas
from ncea.certificate import get_course_endorsement
from project import utils


@user_has_access
@login_required
def list_view(request, **kwargs):
	ctx = {**kwargs}
	ctx = {**ctx, **get_theme(request.user)}
	student = ctx["student"]
	results = get_results(student, date__year=student.viewing_year, include_empty=True)

	subjects = []
	for obj in student.get_subjects(year=student.viewing_year, include_empty=True):
		qs = get_subject_gpas(student, subject=obj)
		gpa = qs.first().get_gpa() if qs.exists() else None
		gpa_change = gpa - qs[1].get_gpa() if len(qs) > 1 else None

		subjects.append({
			"subject": obj,
			"result": results.filter(grade=None, subject=obj, date__gte=timezone.now()).first(),
			"gpa": gpa,
			"gpa_change": f"{gpa_change:+}" if gpa_change != None else gpa_change,
		})
	subjects.sort(key=lambda x: x.get("gpa") or 0, reverse=True)

	ctx["subject_data"] = subjects
	ctx["student_data"] = utils.deep_serialize(student)
	ctx["raw_data"] = utils.deep_serialize(results.exclude(grade=None), max_depth=1)
	return render(request, "insight/list.html", ctx)


@user_has_access
@login_required
def subject_view(request, pk, **kwargs):
	ctx = {**kwargs}
	ctx = {**ctx, **get_theme(request.user)}
	student = ctx["student"]
	subject = get_object_or_404(Subject, pk=pk)
	results = get_results(student, subject=subject, include_empty=True)
		
	# Goals related to this subject
	goal_qs = Goal.objects.filter(student=ctx["student"], date__year__lte=student.to_year(subject.year_level))
	for obj in goal_qs:
		filters = demjson3.decode(obj.filters)
		if filters.get("subject") and filters.get("subject") != subject.subject_code:
			goal_qs = goal_qs.exclude(pk=obj.pk)
	ctx["goal_qs"] = goal_qs

	# Calculate endorsement data
	level, credits = get_course_endorsement(student, subject.subject_code)
	a_sum = sum(credits["a"].values())
	m_sum = sum(credits["m"].values())
	e_sum = sum(credits["e"].values())

	ctx["internalexternal"] = {
		"internal": {
			"a": credits["a"]["i"] + credits["m"]["i"] + credits["e"]["i"],
			"m": credits["m"]["i"] + credits["e"]["i"],
			"e": credits["e"]["i"],
		},
		"external": {
			"a": credits["a"]["e"] + credits["m"]["e"] + credits["e"]["e"],
			"m": credits["m"]["e"] + credits["e"]["e"],
			"e": credits["e"]["e"],
		}
	}

	ctx["progress"] = {
		"a": a_sum + m_sum + e_sum,
		"m": m_sum + e_sum,
		"e": e_sum,
	}

	if level:
		ctx["endorsement_level"] = {
			"a": "Achieve",
			"m": "Merit",
			"e": "Excellence"
		}[level]

	ctx["gpa_qs"] = get_subject_gpas(student, subject=subject)[:8]
	ctx["student_data"] = utils.deep_serialize(student)
	ctx["empty_result_qs"] = results.filter(grade=None, date__gte=utils.localnow())
	ctx["raw_data"] = utils.deep_serialize(results.exclude(grade=None), max_depth=1)
	ctx["subject"] = subject
	return render(request, "insight/subject.html", ctx)



