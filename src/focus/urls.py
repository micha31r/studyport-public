from django.urls import path
from . import views

app_name = "focus"

urlpatterns = [
    path("set", views.set_view, name="set"),
]