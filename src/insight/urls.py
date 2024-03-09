from django.urls import path
from . import views

app_name = "insight"

urlpatterns = [
    path('', views.list_view, name="list"),
    path('subject/<int:pk>', views.subject_view, name="subject"),
]