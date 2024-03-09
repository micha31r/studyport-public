import demjson3
from django.apps import apps
from django.utils import timezone
from standards.models import Subject
from results.conversion import grade_to_GPA
from results.models import Result
from results.utils import calc_gpa
from focus.models import FocusPeriod
from goal.models import Goal

def calc_gpa_override(goal, qs):
	return calc_gpa(qs)


def calc_rankscore(goal, qs):
	value = 0
	for obj in qs:
		if obj.assessment.level >= 3:
			value += obj.assessment.credits * grade_to_GPA(goal.student.grading_system, obj.grade)
	return value


def duration(goal, qs):
	value = 0
	for obj in qs:
		value += obj.duration.total_seconds()
	return value / 60


CALLBACKS = {
	"gpa": calc_gpa_override,
	"rankscore": calc_rankscore,
	"duration": duration,
}


class Validator:
	def __init__(self, goal):
		self.goal = goal
		self.Model = apps.get_model(self.goal.model_name)
		self.filters = {**self.get_filters(), **demjson3.decode(self.goal.filters)}
		self.excludes = self.get_excludes()

	def get_filters(self):
		model_name = self.goal.model_name
		student = self.goal.student
		filters =  {
			"results.Result": {
				"student": student,
				"playground": None,
				"is_mock": False,
				"is_published": True,
			},
			"focus.FocusPeriod": {
				"student": student,
			},
		}

		# Dynamic values

		if self.goal.repeat != "once":
			date_range = self.goal.get_date_range()
			filters["date__gte"] = date_range[0]
			filters["date__lt"] = date_range[1]

		return filters[model_name]

	def get_excludes(self):
		model_name = self.goal.model_name
		student = self.goal.student
		excludes = {
			"results.Result": {
				"grade": None
			},
			"focus.FocusPeriod": {},
		}

		return excludes[model_name]

	def get_queryset(self):
		qs = self.Model.objects.filter(**self.filters).exclude(**self.excludes)
		return qs

	def get_value(self):
		value = 0
		qs = self.get_queryset()

		if self.goal.field in CALLBACKS:
			# If field is a callback function
			value = CALLBACKS[self.goal.field](self.goal, qs)
		else:
			# If field is a model attribute
			path = self.goal.field.split(".")
			for obj in qs:
				for index, name in enumerate(path):
					obj = getattr(obj, name)
					if index == len(path)-1:
						value += obj
		return value

	def reached_deadline(self):
		reached = False
		if self.goal.end_date:
			today = timezone.now().date()
			if today > self.goal.end_date:
				reached = True
		return reached

	def get_status(self):
		current = self.goal.current
		target = self.goal.target
		c = self.goal.comparator
		# if c == "<" and current < target or \
		# 	c == "<=" and current <= target or \
		if c == ">" and current > target or \
			c == ">=" and current >= target or \
			c == "==" and current == target:

			if self.goal.end_option == "before":
				if not self.reached_deadline():
					return "success"
			else:
				if self.reached_deadline():
					return "success"

		if not self.reached_deadline():
			return "ongoing"
		return "fail"

	def update_instance(self):
		if not self.reached_deadline():
			# Progress can only be calculated before the deadline
			self.goal.current = self.get_value()
			self.goal.save()
		self.goal.status = self.get_status()
		# Set completion date
		if self.goal.status == "success":
			self.goal.completion_date = timezone.now()
		self.goal.save()

		











