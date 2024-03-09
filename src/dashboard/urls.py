from django.urls import path, include
from . import views

app_name = "dashboard"

urlpatterns = [
	path('notifications', views.notification_view, name="notification"),
    path('notifications/mark-as-read', views.mark_as_read_view, name="mark-as-read"),
]