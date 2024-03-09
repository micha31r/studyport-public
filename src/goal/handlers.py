from notifications.signals import notify
from stats.models import StreakRecord
from .models import Goal
from .validator import Validator


# Change goal status and send notification 
# sender: Goal
def goal_status_handler(sender, instance, **kwargs):
	v = Validator(instance)
	v.update_instance()

	if v.goal.status == "success":
		notify.send(
			sender = instance,
			recipient = instance.student.user,
			verb = "Congratulations, you have completed a new goal 🎉",
			target = instance,
			notification_type = "goal",
		)
	elif v.goal.status == "fail":
		notify.send(
			sender = instance,
			recipient = instance.student.user,
			verb = "You failed to complete a goal, better luck next time",
			target = instance,
			notification_type = "goal",
		)


# sender: Result
def result_proxy_goal_status_handler(sender, instance, **kwargs):
	qs = Goal.objects.filter(student=instance.student, status="ongoing", model_name="results.Result")
	for obj in qs:
		goal_status_handler(sender=Goal, instance=obj)


# sender: FocusPeriod
def focus_period_proxy_goal_status_handler(sender, instance, **kwargs):
	qs = Goal.objects.filter(student=instance.student, status="ongoing", model_name="focus.FocusPeriod")
	for obj in qs:
		goal_status_handler(sender=Goal, instance=obj)


# Calculate goal streak
# sender: Goal
def goal_streak_handler(sender, instance, **kwargs):
	qs = Goal.objects.filter(student=instance.student)

	items = {}
	for obj in qs.exclude(status="ongoing"):
		if obj.repeat == "once":
			key = str(obj.completion_date) if obj.status == "success" else str(obj.end_date)
			if key in items:
				key += str(obj.pk)
			items[key] = obj

	sorted_items = []
	for key in sorted(items):
		sorted_items.append(items[key])

	streak_data = [None] * 9

	for index, obj in enumerate(sorted_items[-9:]):
		if obj.repeat == "once":
			streak_data[index] = obj

	# Count streak
	counter = 0
	for index, item in enumerate(streak_data):
		if item != None:
			if item.status == "success":
				counter += 1
			else:
				counter = 0
				streak_data[index] = None

	streak_obj = instance.student.get_highest_streak("goal")
	prev_highest = streak_obj.count if streak_obj else 0
	if counter > prev_highest:
		StreakRecord.objects.create(
			student = instance.student,
			streak_type = "goal",
			count = counter
		)






