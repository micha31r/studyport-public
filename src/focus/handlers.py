from datetime import timedelta
from django.utils import timezone
from notifications.signals import notify
from stats.models import StreakRecord
from .models import FocusPeriod


# Calculate focus streak
# sender: FocusPeriod
def focus_streak_handler(sender, instance, **kwargs):
	qs = FocusPeriod.objects.filter(student=instance.student, duration__gte=timedelta(minutes=20)).order_by("date")

	data = {}
	if qs.count() > 0:
		max_date = qs[qs.count()-1].date
		min_date = qs.first().date
		start_date = max_date if (max_date - min_date).days >= 9 else min_date + timedelta(days=8)
	else:
		start_date = timezone.now().date()

	for i in range(9):
		data[str(start_date - timedelta(days=i))] = None

	for obj in qs.filter(date__year=timezone.now().date().year)[:9]:
		if str(obj.date) in data:
			data[str(obj.date)] = obj

	# Count streak
	counter = 0
	for item in reversed(data.values()):
		if item: counter += 1
		else: counter = 0

	streak_obj = instance.student.get_highest_streak("focus")
	prev_highest = streak_obj.count if streak_obj else 0


	if streak_obj and instance.date == streak_obj.datetime.date():
		streak_obj.count = counter
		streak_obj.datetime = timezone.now()
		streak_obj.save()
	else:
		StreakRecord.objects.create(
			student = instance.student,
			streak_type = "focus",
			count = counter
		)


