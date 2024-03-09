from notifications.signals import notify
from stats.models import YearGPA, SubjectGPA
from .models import Result
from .utils import get_results, calc_gpa


# Calculate GPA
# sender: Result
def gpa_handler(sender, instance, **kwargs):
	if instance.grade:
		playground = None
		if instance.student.playground_is_active:
			playground = instance.student.get_playground()

		qs = get_results(
			instance.student,
			date__year = instance.date.year,
			ignore_visibility = True,
			is_published = True,
		)

		YearGPA.objects.get_or_create(
			student = instance.student,
			playground = playground,
			gpa = calc_gpa(qs.filter(is_mock=False)),
			mock_gpa = calc_gpa(qs),
			year = instance.date.year
		)

		qs = get_results(
			instance.student,
			subject = instance.subject,
			ignore_visibility = True,
			is_published = True,
		)

		SubjectGPA.objects.get_or_create(
			student = instance.student,
			playground = playground,
			gpa = calc_gpa(qs.filter(is_mock=False)),
			mock_gpa = calc_gpa(qs),
			subject = instance.subject
		)


# Recent activities
def recent_activity_handler(sender, instance, **kwargs):
	notify.send(
		sender = Result,
		recipient = instance.student.user,
		verb = "A new result has been released",
		action_object = instance,
	)


# Upcoming assessments
def upcoming_assessment_handler(sender, instance, **kwargs):
	notify.send(
		sender = Result,
		recipient = instance.student.user,
		verb = "Upcoming assessment",
		action_object = instance,
	)