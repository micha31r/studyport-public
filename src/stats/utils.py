from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
from .models import SubjectGPA, YearGPA


# Create a date range
def date_range(start, end=timezone.now().date()):
	result = [];
	for i in range(int((end - start).days)):
		result.append(start + timezone.timedelta(days=i))
	return result


"""
When playground is active:
 - Get all objects

When playground is not active:
 - Only get original objects

"""


def get_subject_gpas(student, **kwargs):
	qs = SubjectGPA.objects.filter(student=student, **kwargs).order_by("-datetime")
	if not student.playground_is_active:
		qs = qs.filter(playground=None)
	return qs


def get_year_gpas(student, **kwargs):
	qs = YearGPA.objects.filter(student=student, **kwargs).order_by("-datetime")
	if not student.playground_is_active:
		qs = qs.filter(playground=None)
	return qs
