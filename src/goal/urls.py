from django.urls import path
from . import views

app_name = "goal"

urlpatterns = [
    path("", views.list_view, name="list"),
    path("detail/<int:pk>", views.detail_view, name="detail"),
    path("create/credits", views.create_credits_view, name="create-credits"),
    path("create/gpa", views.create_gpa_view, name="create-gpa"),
    path("create/rank-score", views.create_rank_score_view, name="create-rank-score"),
    path("create/focus-period", views.create_focus_period_view, name="create-focus-period"),
    path("edit/<int:pk>", views.edit_view, name="edit"),
    path("delete/<int:pk>", views.delete_view, name="delete"),
]