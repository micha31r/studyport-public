from datetime import timedelta
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from results.models import Result
from results.utils import get_results
from usermgmt.models import Student
from usermgmt.decorators import user_has_access
from settings.themes import get_theme
from project import utils
from goal.models import Goal
from focus.models import FocusPeriod
import json

from results.models import Result
from stats.utils import get_year_gpas


@method_decorator(login_required, name='dispatch')
@method_decorator(user_has_access, name='dispatch')
class BaseView(TemplateView):
    template_name = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx = {**ctx, **get_theme(self.request.user)}

        student = ctx["student"]
        self.results = get_results(student, date__year=student.viewing_year, include_empty=True)

        ctx["goals"] = Goal.objects.filter(student=student, status="ongoing")
        ctx["student_data"] = utils.deep_serialize(student)
        ctx["raw_data"] = utils.deep_serialize(self.results.exclude(grade=None), max_depth=1)
        return ctx


class OverviewView(BaseView):
    template_name = "stats/overview.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = ctx["student"]

        # Empty results are all upcoming assessments
        ctx["empty_results"] = self.results.filter(grade=None, date__gte=utils.localnow())

        # Rank score is only calculated on NCEA level 3 results
        ctx["rank_score_data"] = utils.deep_serialize(get_results(student, assessment__level=3), max_depth=1)
        ctx["gpa"] = get_year_gpas(student, year=student.viewing_year).first()
        return ctx


class AcademicProgressView(BaseView):
    template_name = "stats/progress/academic.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = ctx["student"]
        ctx["year_level_gpa_qs"] = get_year_gpas(student, year=student.viewing_year)
        return ctx


class GoalProgressView(BaseView):
    template_name = "stats/progress/goal.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = ctx["student"]
        qs = Goal.objects.filter(student=student)
        ctx["goal_data"] = utils.deep_serialize(qs, max_depth=1)
        # ctx["highest_streak"] = highest_streak_obj.count if highest_streak_obj else 0
        return ctx


class FocusProgressView(BaseView):
    template_name = "stats/progress/focus.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = ctx["student"]
        qs = FocusPeriod.objects.filter(student=student).order_by("date")
        ctx["focus_data"] = utils.deep_serialize(qs, max_depth=1)
        ctx["today"] = timezone.now().date()

        # Calculate weekly total

        weekly_total = 0
        weekday = utils.localnow().isocalendar()[2]
        min_date = utils.localnow().date() - timedelta(days=weekday - 1)
        max_date = utils.localnow().date() + timedelta(days=7 - weekday)
        for obj in qs.filter(date__gte=min_date, date__lte=max_date):
            weekly_total += obj.to_minutes()
        ctx["weekly_total"] = weekly_total

        """
        Calculate focus streak

        1. Get all focus objects with duration more than 20 minutes
        2. Order objects from most recent to least recent
        3. Create empty array new Array(9)
        4. Calculate the difference between the object(n) and object(n-1) and decrease index by this amount
        5. if condition: Assign the object to the corresponding index in the array
        6. Repeat 1-5 until index is less than 0
        """

        qs = qs.filter(date__year=timezone.now().date().year, duration__gte=timedelta(minutes=20)).order_by("-date")
        streak = [False for i in range(9)]
        index = 8
        for obj_index in range(len(qs)):
            if obj_index > 0:
                n1 = qs[obj_index-1].date
            else:
                n1 = utils.localnow().date()
            n2 = qs[obj_index].date
            difference = abs((n2 - n1).days)
            index -= difference
            if index < 0:
                break
            elif qs[obj_index].duration.seconds >= 1200:
                streak[index] = True

        streak_count = 0
        for item in reversed(streak):
            if item == False:
                break
            streak_count += 1

        ctx["streak_count"] = streak_count
        ctx["streak_data"] = streak

        highest_streak_obj = student.get_highest_streak("focus")
        ctx["highest_streak"] = highest_streak_obj.count if highest_streak_obj else 0
        return ctx


class SubjectComparisonView(BaseView):
    template_name = "stats/subject_comparison.html"


class UnitComparisonView(BaseView):
    template_name = "stats/unit_comparison.html"



