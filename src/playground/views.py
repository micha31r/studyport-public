import importlib
import stats.views
from django.utils import timezone
from django.conf import settings
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponseServerError
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usermgmt.models import Student
from usermgmt.decorators import user_has_access
from settings.themes import get_theme
from standards.models import Subject, Assessment
from results.models import Result
from .models import Playground
from .forms import EditForm


@user_has_access
@login_required
def list_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	qs = Playground.objects.filter(student=student)
	ctx["playground_qs"] = qs
	return render(request, "playground/list.html", ctx)


@user_has_access
@login_required
def activate_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	backlink = request.GET.get("backlink")

	# Activate recent playground or redirect to create page
	is_successful = student.activate_playground()
	if is_successful:
		messages.info(request, "Activated playground.")
	else:
		messages.info(request, "Please create a new playground.")
		return redirect("/app/playground/create/True?backlink=" + backlink, activate=True)

	if backlink:
		return redirect(backlink)
	return redirect("playground:list")


@user_has_access
@login_required
def select_view(request, pk, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	backlink = request.GET.get("backlink")

	# Activate recent playground or redirect to create page
	obj = get_object_or_404(Playground, student=student, pk=pk)
	student.recent_playground_id = obj.pk
	student.save()
	messages.success(request, f"Successfully selected playground - \"{obj.name}\".")

	if backlink:
		return redirect(backlink)
	return redirect("playground:list")


@user_has_access
@login_required
def deactivate_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	backlink = request.GET.get("backlink")
	student.deactivate_playground()
	messages.info(request, "Deactivated playground.")

	if backlink:
		return redirect(backlink)
	return redirect("playground:list")


@user_has_access
@login_required
def create_view(request, activate=False, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]

	if request.POST:
		form = EditForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			obj = Playground.objects.create(
				student = student,
				name = data.get("name")
			)
			if bool(activate):
				student.activate_playground()

			messages.success(request, "Successfully created playground.")
			return redirect("playground:list")

	ctx["form"] = EditForm(initial={
		"name": "New Playground"
	})
	return render(request, "playground/create.html", ctx)


@user_has_access
@login_required
def edit_view(request, pk, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	obj = get_object_or_404(Playground, student=student, pk=pk)

	if request.POST:
		form = EditForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			obj.name = data.get("name")
			obj.save()

			messages.success(request, "Successfully updated playground.")

	ctx["obj"] = obj
	ctx["form"] = EditForm(instance=obj)
	return render(request, "playground/edit.html", ctx)


@user_has_access
@login_required
def delete_view(request, pk, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	get_object_or_404(Playground, student=student, pk=pk).delete()
	messages.success(request, "Successfully deleted playground.")
	return redirect("playground:list")




