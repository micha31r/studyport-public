from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView


def home_view(request):
    return redirect("usermgmt:login")


class PrivacyView(TemplateView):
    template_name = "privacy.html"


class RobotsView(TemplateView):
    template_name = "robots.txt"


def handler404(request, exception=None):
	return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)