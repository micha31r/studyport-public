import datetime, uuid, json
from django.utils import timezone, dateformat
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from project import utils
from usermgmt.decorators import user_has_access
from results.utils import get_results
from settings.themes import get_theme
from standards.models import Subject
from usermgmt.models import Student
from .models import Goal, GoalRecord
from .forms import EditorForm, CreditsTemplateForm, GPATemplateForm, RankScoreTemplateForm, FocusPeriodTemplateForm
from .handlers import goal_status_handler


FILTER_VALUE_VALIDATORS = {
	"assessment__level": [
		{
			"callback": lambda v: int(v) in [1, 2, 3],
			"expected": True,
		},
	],
	"subject__subject_code": [],
	"grade": [
		{
			"callback": lambda v: v in ["na", "a", "m", "e"],
			"expected": True,
		},
	],
	"grade__in": [
		{
			"callback": lambda v: [x for x in v if x not in ["a", "m", "e"]],
			"expected": [],
		},
	],
	"date__year": [],
}

def filter_is_valid(filters):
	for k, v in filters.items():
		validators = FILTER_VALUE_VALIDATORS[k]
		for item in validators:
			if item["callback"](v["value"]) != item["expected"]:
				return False
	return True


def create_filter_string(filters):
	obj = {}
	if filter_is_valid(filters):
		for k, v in filters.items():
			string = k
			if v["comparator"] == "<":
				string += "__lt"
			elif v["comparator"] == "<=":
				string += "__lte"
			elif v["comparator"] == ">":
				string += "__gt"
			elif v["comparator"] == ">=":
				string += "__gte"
			obj[string] = v["value"]
	return str(obj)


@login_required
@user_has_access
def list_view(request, **kwargs):
	ctx = {**kwargs}
	ctx = {**ctx, **get_theme(request.user)}

	if request.POST:
		form = EditorForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			obj = form.save(commit=False)
			obj.student = ctx["student"]
			obj.filters = create_filter_string(json.loads(data.get("filters")))
			obj.save()

			# Manually trigger handler
			goal_status_handler(Goal, obj)
			messages.success(request, "Successfully created goal.")
			
	form = EditorForm(initial={
		"date": dateformat.format(timezone.now(), 'Y-m-d')
	})

	qs = Goal.objects.filter(student=ctx["student"])
	repeat = {}
	for obj in qs:
		if obj.repeat not in repeat:
			repeat[obj.repeat] = []
		repeat[obj.repeat].append(obj)
		
	ctx["repeat"] = repeat
	ctx["form"] = form
	template_file = "goal/list.html"
	return render(request, template_file, ctx)


@login_required
@user_has_access
def detail_view(request, pk, **kwargs):
	ctx = {**kwargs}
	ctx = {**ctx, **get_theme(request.user)}
	student = ctx["student"]
	results = get_results(student, date__year=student.viewing_year, include_empty=True)
	ctx["obj"] = goal_obj = get_object_or_404(Goal, pk=pk, student=student)

	ctx["student_data"] = utils.deep_serialize(student)
	ctx["raw_data"] = utils.deep_serialize(results.exclude(grade=None), max_depth=1)
	ctx["goal_data"] = utils.deep_serialize(goal_obj.goalrecord_set.order_by("date")[:14], max_depth=1)

	template_file = "goal/detail.html"
	return render(request, template_file, ctx)


@login_required
@user_has_access
def create_credits_view(request, **kwargs):
	ctx = {**kwargs}
	ctx = {**ctx, **get_theme(request.user)}
	student = ctx["student"]

	# Get subject options
	qs = Subject.objects.all()
	data = {}
	for item in qs:
		data[item.name] = item.subject_code
	ctx["subject_data"] = data

	if request.POST:
		form = CreditsTemplateForm(student, request.POST)
		if form.is_valid():
			data = form.cleaned_data
			filters = {}
			
			if data.get("grade") == "*":
				# Filter by all passing grades
				choices = form.NCEA_CHOICES
				if student.grading_system == "alphabetical":
					choices = form.ALPHABET_CHOICES
				passing_grades = [x[0] for x in choices if x[0] not in ["na", "f"]]
				filters["grade__in"] = passing_grades
			else:
				filters["grade"] = data.get("grade")

			if data.get("subject_code"):
				filters["subject__subject_code"] = data.get("subject_code")

			if data.get("year"):
				filters["date__year"] = data.get("year")

			obj = Goal.objects.create(
				student = student,
				target = data.get("target"),
				field = "assessment.credits",
				comparator = ">=",
				model_name = "results.Result",
				filters = str(filters),
				end_date = data.get("end_date"),
				end_option = "before",
			)

			# Manually trigger handler
			goal_status_handler(Goal, obj)
			messages.success(request, "Successfully created goal.")
			return redirect("goal:list")
			
	form = CreditsTemplateForm(student, initial={
		"year": timezone.now().date().year
	})
		
	ctx["form"] = form
	template_file = "goal/create-credits.html"
	return render(request, template_file, ctx)


@login_required
@user_has_access
def create_gpa_view(request, **kwargs):
	ctx = {**kwargs}
	ctx = {**ctx, **get_theme(request.user)}
	student = ctx["student"]

	# Get subject options
	qs = Subject.objects.all()
	data = {}
	for item in qs:
		data[item.name] = item.subject_code
	ctx["subject_data"] = data

	if request.POST:
		form = GPATemplateForm(student, request.POST)
		if form.is_valid():
			data = form.cleaned_data
			filters = {}

			if data.get("subject_code"):
				filters["subject__subject_code"] = data.get("subject_code")

			if data.get("year"):
				filters["date__year"] = data.get("year")

			obj = Goal.objects.create(
				student = student,
				target = data.get("target"),
				field = "gpa",
				comparator = ">=",
				model_name = "results.Result",
				filters = str(filters),
				end_date = data.get("end_date"),
				end_option = "after",
			)

			# Manually trigger handler
			goal_status_handler(Goal, obj)
			messages.success(request, "Successfully created goal.")
			return redirect("goal:list")
			
	form = GPATemplateForm(student, initial={
		"year": timezone.now().date().year
	})
		
	ctx["form"] = form
	template_file = "goal/create-gpa.html"
	return render(request, template_file, ctx)


@login_required
@user_has_access
def create_rank_score_view(request, **kwargs):
	ctx = {**kwargs}
	ctx = {**ctx, **get_theme(request.user)}
	student = ctx["student"]

	# Get subject options
	qs = Subject.objects.all()
	data = {}
	for item in qs:
		data[item.name] = item.subject_code
	ctx["subject_data"] = data

	if request.POST:
		form = RankScoreTemplateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			filters = {}

			if data.get("subject_code"):
				filters["subject__subject_code"] = data.get("subject_code")

			obj = Goal.objects.create(
				student = student,
				target = data.get("target"),
				field = "rankscore",
				comparator = ">=",
				model_name = "results.Result",
				filters = str(filters),
				end_date = data.get("end_date"),
				end_option = "before",
			)

			# Manually trigger handler
			goal_status_handler(Goal, obj)
			messages.success(request, "Successfully created goal.")
			return redirect("goal:list")
			
	form = RankScoreTemplateForm()
		
	ctx["form"] = form
	template_file = "goal/create-rank-score.html"
	return render(request, template_file, ctx)


@login_required
@user_has_access
def create_focus_period_view(request, **kwargs):
	ctx = {**kwargs}
	ctx = {**ctx, **get_theme(request.user)}
	student = ctx["student"]

	# Get subject options
	qs = Subject.objects.all()
	data = {}
	for item in qs:
		data[item.name] = item.subject_code
	ctx["subject_data"] = data

	if request.POST:
		form = FocusPeriodTemplateForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			filters = {}

			obj = Goal.objects.create(
				student = student,
				target = data.get("target"),
				field = "duration",
				comparator = ">=",
				model_name = "focus.FocusPeriod",
				filters = str(filters),
				repeat = data.get("repeat"),
				end_date = data.get("end_date"),
				end_option = "before",
			)

			# Manually trigger handler
			goal_status_handler(Goal, obj)
			messages.success(request, "Successfully created goal.")
			return redirect("goal:list")
			
	form = FocusPeriodTemplateForm()
		
	ctx["form"] = form
	template_file = "goal/create-focus-period.html"
	return render(request, template_file, ctx)


@login_required
@user_has_access
def edit_view(request, pk, **kwargs):
	ctx = {**kwargs}
	ctx = {**ctx, **get_theme(request.user)}

	obj = get_object_or_404(Goal, student=ctx["student"], pk=pk)

	if request.POST:
		form = EditorForm(request.POST, instance=obj)
		if form.is_valid():
			obj = form.save()
			obj.filters = create_filter_string(json.loads(form.cleaned_data.get("filters")))
			obj.save()
			
			# Manually trigger handler
			goal_status_handler(Goal, obj)
			messages.success(request, "Successfully updated goal.")
			
	ctx["form"] = EditorForm(instance=obj)
	ctx["obj"] = obj
	template_file = "goal/edit.html"
	return render(request, template_file, ctx)


@user_has_access
@login_required
def delete_view(request, pk, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	get_object_or_404(Goal, student=student, pk=pk).delete()
	messages.success(request, "Successfully deleted goal.")
	return redirect("goal:list")


