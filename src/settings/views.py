import datetime, uuid
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import FormView
from django.http import Http404
from django.urls import reverse
from verification.models import Verification
from group.models import School
from results.models import Result
from usermgmt.models import Student
from usermgmt.decorators import user_has_access
from .themes import CHART_PALETTE
from .models import ColorSettings
from .forms import *


@user_has_access
@login_required
def app_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]

	if request.POST:
		form = AppForm(request.POST, instance=student)
		if form.is_valid():
			show_mock_results = student.show_mock_results
			form.save()
			new_image = form.cleaned_data.get("profile_image")
			if new_image != student.profile_image:
				student.profile_image = new_image
				student.save()
			messages.success(request, "Successfully updated app settings.")

	ctx["form"] = form = AppForm(instance=student, initial={
		"profile_image": student.profile_image
	})
	return render(request, "settings/app.html", ctx)


@user_has_access
@login_required
def account_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]

	if request.POST:
		form = AccountForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			student.user.first_name = data.get("first_name")
			student.user.last_name = data.get("last_name")
			student.user.email = data.get("email")
			student.student_id = data.get("student_id")
			student.user.save()
			student.save()
			messages.success(request, "Successfully updated account information.")

	ctx["form"] = AccountForm(initial={
		"first_name": student.user.first_name,
		"last_name": student.user.last_name,
		"student_id": student.student_id,
		"email": student.user.email,
	})
	return render(request, "settings/account.html", ctx)


@user_has_access
@login_required
def password_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]

	if request.POST:
		form = PasswordForm(request.POST, user=request.user)
		if form.is_valid():
			if request.user.has_usable_password():
				cp = data.get("current_password")
				user = authenticate(request, username=student.user.username, password=cp)
			else:
				# Skip require current password verification the first time for oauth users
				user = request.user
			if user:
				np = data.get("new_password")
				if np == data.get("confirm_password"):
					user.set_password(np)
					user.save()
					messages.success(request, "Successfully changed password.")

	ctx["form"] = PasswordForm(user=request.user)
	return render(request, "settings/password.html", ctx)


@user_has_access
@login_required
def theme_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]

	FormClass = NCEAThemeForm
	if student.grading_system == "alphabetical":
		FormClass = AlphabetThemeForm
	
	if request.POST:
		form = FormClass(request.POST, instance=student.color_settings)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully updated themes.")

	ctx["form"] = FormClass(instance=student.color_settings)
	ctx["chart_swatches"] = CHART_PALETTE
	return render(request, "settings/theme.html", ctx)


@user_has_access
@login_required
def show_mock_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	student.show_mock_results = True
	student.save()
	messages.info(request, "Mock exam results are now visible.")

	backlink = request.GET.get("backlink")

	if backlink:
		return redirect(backlink)
	return redirect("stats:overview")


@user_has_access
@login_required
def hide_mock_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]
	student.show_mock_results = False
	student.save()
	messages.info(request, "Mock exam results are now hidden.")

	backlink = request.GET.get("backlink")

	if backlink:
		return redirect(backlink)
	return redirect("stats:overview")