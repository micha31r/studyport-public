"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views

import usermgmt.views as usermgmt_views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("privacy", views.PrivacyView.as_view(), name="privacy"),
    path("robots.txt", views.RobotsView.as_view(content_type="text/plain"), name="robots"),
    path("accounts/google/login/", usermgmt_views.custom_oauth2_login),
    path("accounts/google/login/callback/", usermgmt_views.custom_oauth2_callback),
    path("accounts/", include("allauth.urls")),
    path("404", views.handler404, name="404"),
    path("500", views.handler500, name="500"),
    path("user/", include("usermgmt.urls")),
    path("app/", include("dashboard.urls")),
    path("app/stats/", include("stats.urls")),
    path("app/settings/", include("settings.urls")),
    path("app/results/", include("results.urls")),
    path("app/playground/", include("playground.urls")),
    path("app/ncea/", include("ncea.urls")),
    path("app/insights/", include("insight.urls")),
    path("app/goal/", include("goal.urls")),
    path("app/focus/", include("focus.urls")),
    path("docs/", include("docs.urls")),
    path('inbox/notifications/', include("notifications.urls", namespace='notifications')),
    path("admin/", admin.site.urls)
]

handler404 = views.handler404
handler500 = views.handler500

# if settings.DEBUG:
    # urlpatterns.append(path("admin/", admin.site.urls))
