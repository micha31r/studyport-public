from django.urls import path
from . import views

app_name = "ncea"

urlpatterns = [
    path('<str:level>', views.summary_view, name="summary"),
]