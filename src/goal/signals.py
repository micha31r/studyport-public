from django.db.models.signals import post_save, post_delete
from focus.models import FocusPeriod
from results.models import Result
from .models import Goal
from .handlers import *


# Goal status
post_save.connect(result_proxy_goal_status_handler, sender=Result)
post_delete.connect(result_proxy_goal_status_handler, sender=Result)

# Goal status
post_save.connect(focus_period_proxy_goal_status_handler, sender=FocusPeriod)
post_delete.connect(focus_period_proxy_goal_status_handler, sender=FocusPeriod)

# Goal Streak
post_save.connect(goal_streak_handler, sender=Goal)