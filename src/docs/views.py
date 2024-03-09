from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from usermgmt.decorators import user_has_access
from settings.themes import get_theme


@method_decorator(login_required, name='dispatch')
@method_decorator(user_has_access, name='dispatch')
class BaseView(TemplateView):
    template_name = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx = {**ctx, **get_theme(self.request.user)}
        return ctx


class CatalogView(BaseView):
    template_name = "docs/catalog.html"

class NCEAView(BaseView):
	template_name = "docs/ncea.html"

class GoalsView(BaseView):
    template_name = "docs/goals.html"

class InsightsView(BaseView):
    template_name = "docs/insights.html"

class OverviewView(BaseView):
    template_name = "docs/overview.html"

class PlaygroundView(BaseView):
    template_name = "docs/playground.html"

class ResultsView(BaseView):
    template_name = "docs/results.html"

class ProgressAcademicView(BaseView):
    template_name = "docs/progress-academic.html"

class ProgressGoalView(BaseView):
    template_name = "docs/progress-goal.html"

class ProgressFocusView(BaseView):
    template_name = "docs/progress-focus.html"



