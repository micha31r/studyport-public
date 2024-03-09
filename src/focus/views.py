import datetime
from django.utils import timezone, dateformat
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usermgmt.decorators import user_has_access
from settings.themes import get_theme
from standards.models import Subject
from usermgmt.models import Student
from .models import FocusPeriod


@user_has_access
@login_required
def set_view(request, **kwargs):
	ctx = {**kwargs}
	student = ctx["student"]

	obj = FocusPeriod.objects.filter(student=student, date=timezone.now()).first()
	if not obj:
		obj = FocusPeriod.objects.create(
			student = student,
			duration = datetime.timedelta(),
		)

	value = request.POST.get("duration")
	if value and value.replace(".", "", 1).isdigit():
		obj.duration = datetime.timedelta(minutes=float(value))
		obj.save()
		messages.success(request, "Successfully set focus period.")

	backlink = request.GET.get("backlink")
	if backlink:
		return redirect(backlink)
	return redirect("stats:overview")