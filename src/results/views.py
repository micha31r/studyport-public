import importlib
import stats.views
from django.utils import timezone
from django.conf import settings
from django.core import serializers
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponseServerError
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usermgmt.models import Student
from usermgmt.decorators import user_has_access
from settings.themes import get_theme
from standards.models import Subject, Assessment
from .models import Result
from .forms import FilterForm, NCEAEditForm, AlphabetEditForm
from .utils import get_results, year_passed, year_endorsed, course_endorsed


@user_has_access
@login_required
def list_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	qs = get_results(student, include_empty=True, ignore_visibility=True)

	initial = {}
	
	if request.POST:
		form = FilterForm(student, request.POST)
		if form.is_valid():
			initial["year"] = year = form.cleaned_data.get("year")
			initial["wildcard"] = wildcard = form.cleaned_data.get("wildcard")
			query = Q(subject__subject_code__icontains = wildcard) | \
					Q(subject__name__icontains = wildcard) | \
					Q(subject__department__icontains = wildcard) | \
					Q(assessment__assessment_code__icontains = wildcard) | \
					Q(assessment__title__icontains = wildcard) | \
					Q(assessment__assessment_type__icontains = wildcard)
			if year:
				query = query & Q(date__year=year)
			qs = qs.filter(query)
			messages.info(request, f"Filtered results {'by year ' + year if year else ''} {'with query: '+ wildcard if wildcard else ''}")

	data = {}
	for obj in qs:
		level = obj.student.to_year_level(obj.date.year)
		if level not in data:
			data[level] = []
		data[level].append(obj)

	ctx["form"] = FilterForm(student, initial=initial)
	ctx["data"] = data
	return render(request, "results/list.html", ctx)


@user_has_access
@login_required
def edit_view(request, pk, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	obj = get_object_or_404(Result, student=student, pk=pk)

	# Manually redirect to alias object if playground is active
	if student.playground_is_active and getattr(obj, "reverse_play_source", None):
		return redirect("results:edit", pk=obj.reverse_play_source.pk)

	# Get subject options
	qs = Subject.objects.all()
	data = {}
	for item in qs:
		data[item.name] = item.subject_code
	ctx["subject_data"] = data

	# Get assessment options
	qs = Assessment.objects.all()
	data = {}
	for item in qs:
		data[item.title] = item.assessment_code
	ctx["assessment_data"] = data

	FormClass = NCEAEditForm
	if student.grading_system == "alphabetical":
		FormClass = AlphabetEditForm
	
	if request.POST:
		form = FormClass(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			subject = Subject.objects.filter(subject_code=data.get("subject_code")).first()
			assessment = Assessment.objects.filter(assessment_code=data.get("assessment_code")).first()
			if subject and assessment:
				grade = data.get("grade")
				if grade == "":
					grade = None
				obj.subject = subject
				obj.assessment = assessment
				obj.date = data.get("date").date()
				obj.grade = grade
				obj.is_mock = data.get("is_mock")
				obj.is_published = data.get("is_published")
				obj.save()

				messages.success(request, "Successfully updated result entry.")

	form = FormClass(initial={
		"subject_code": obj.subject.subject_code,
		"assessment_code": obj.assessment.assessment_code,
		"date": obj.date,
		"grade": obj.grade,
		"is_mock": obj.is_mock,
		"is_published": obj.is_published,
	})

	ctx["obj"] = obj
	ctx["form"] = form
	return render(request, "results/edit.html", ctx)


@user_has_access
@login_required
def create_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]

	# Get subject options
	qs = Subject.objects.all()
	data = {}
	for item in qs:
		data[item.name] = item.subject_code
	ctx["subject_data"] = data

	# Get assessment options
	qs = Assessment.objects.all()
	data = {}
	for item in qs:
		data[item.title] = item.assessment_code
	ctx["assessment_data"] = data

	FormClass = NCEAEditForm
	if student.grading_system == "alphabetical":
		FormClass = AlphabetEditForm
	
	if request.POST:
		form = FormClass(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			subject = Subject.objects.filter(subject_code=data.get("subject_code")).first()
			assessment = Assessment.objects.filter(assessment_code=data.get("assessment_code")).first()
			if subject and assessment:
				grade = data.get("grade")
				if grade == "":
					grade = None
				obj = Result.objects.create(
					student = student,
					subject = subject,
					assessment = assessment,
					date = data.get("date"),
					grade = grade,
					is_mock = data.get("is_mock"),
					is_published = data.get("is_published"),
				)
				# response = redirect("results:edit", pk=obj.pk)
				# response['Location'] += '?backlink=' + request.GET.get("backlink")
				messages.success(request, "Successfully create new result entry.")
				return redirect("results:list")

	form = FormClass(initial={
		"is_published": True,
	})
	ctx["form"] = form
	return render(request, "results/create.html", ctx)


@user_has_access
@login_required
def delete_view(request, pks, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	if student.playground_is_active:
		messages.error(request, "Playground must be disabled to delete results.")
	else:
		pks = pks.split(",")
		qs = Result.objects.filter(student=student, pk__in=pks).delete()
		messages.success(request, "Successfully deleted result entry.")
	return redirect("results:list")

