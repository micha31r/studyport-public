from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from background_task import background
from background_task.models import Task
from .models import Goal, GoalRecord

@background(schedule=0)
def create_goal_records():
	today = timezone.now().date()
	qs = Goal.objects.all()
	for obj in qs:
		if today >= obj.get_date_range()[1]:
			obj.reset()

if not Task.objects.filter(verbose_name="create_goal_records").exists():
	create_goal_records(repeat=Task.DAILY, verbose_name="create_goal_records", repeat_until=None)
