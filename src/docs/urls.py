from django.urls import path
from . import views

app_name = "docs"

urlpatterns = [
    path('catalog', views.CatalogView.as_view(), name="catalog"),
    path('ncea', views.NCEAView.as_view(), name="ncea"),
    path('goals', views.GoalsView.as_view(), name="goals"),
    path('insights', views.InsightsView.as_view(), name="insights"),
    path('overview', views.OverviewView.as_view(), name="overview"),
    path('playground', views.PlaygroundView.as_view(), name="playground"),
    path('results', views.ResultsView.as_view(), name="results"),
    path('progress/academic', views.ProgressAcademicView.as_view(), name="progress-academic"),
    path('progress/goal', views.ProgressGoalView.as_view(), name="progress-goal"),
    path('progress/focus', views.ProgressFocusView.as_view(), name="progress-focus"),
]