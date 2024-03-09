from django.urls import path
from . import views

app_name = "stats"

urlpatterns = [
    path('overview', views.OverviewView.as_view(), name="overview"),
    path('overview/<str:username>', views.OverviewView.as_view(), name="overview"),
    path('progress/academic', views.AcademicProgressView.as_view(), name="progress-academic"),
    path('progress/goal', views.GoalProgressView.as_view(), name="progress-goal"),
    path('progress/focus', views.FocusProgressView.as_view(), name="progress-focus"),
    path('progress/academic/<str:username>', views.AcademicProgressView.as_view(), name="progress-academic"),
    path('progress/goal/<str:username>', views.GoalProgressView.as_view(), name="progress-goal"),
    path('progress/focus/<str:username>', views.FocusProgressView.as_view(), name="progress-focus"),
    path('subject-comparison', views.SubjectComparisonView.as_view(), name="subject-comparison"),
    path('subject-comparison/<str:username>', views.SubjectComparisonView.as_view(), name="subject-comparison"),
    path('unit-comparison', views.UnitComparisonView.as_view(), name="unit-comparison"),
    path('unit-comparison/<str:username>', views.UnitComparisonView.as_view(), name="unit-comparison"),
]