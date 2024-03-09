from django.urls import path
from . import views

app_name = "connect"

urlpatterns = [
    path("", views.handler_view, name="handler"),
]