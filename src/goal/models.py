import demjson3
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from django.apps import apps


class GoalRecord(models.Model):
	STATUS_CHOICES = (
	    ("success", "Success"),
	    ("fail", "Failed"),
	)

	goal = models.ForeignKey(
		"goal.Goal",
		on_delete=models.CASCADE,
	)

	value = models.FloatField(blank=True, null=True)
	status = models.CharField(choices=STATUS_CHOICES, default="ongoing", max_length=255)
	cycle = models.IntegerField(default=0)
	date = models.DateField(default=timezone.now)


# Example goals
# 4.00 GPA for subject "MAC3" before 31/12/2022
# 105 credits of type "e" for "*" before 31/12/2022

class Goal(models.Model):
	FIELD_CHOICES = (
	    ("assessment.credits", "Credits"),
	    ("gpa", "GPA"),
	    ("rankscore", "Rank Score"),
	    ("duration", "Focus Period"),
	)

	MODEL_NAME_CHOICES = (
	    ("results.Result", "Result"),
	    ("focus.FocusPeriod", "FocusPeriod"),
	)

	STATUS_CHOICES = (
	    ("ongoing", "Ongoing"),
	    ("success", "Success"),
	    ("fail", "Failed"),
	)

	REPEAT_CHOICES = (
	    ("once", "Once"),
	    ("weekly", "Weekly"),
	    ("monthly", "Monthly"),
	)

	END_OPTION_CHOICES = (
	    ("before", "Can End Before"),
	    ("after", "Must End After"),
	)

	COMPARITOR_CHOICES = (
	    # ("<", "less than"),
	    # ("<=", "less than or equal to"),
	    (">", "more than"),
	    (">=", "more than or equal to"),
	    ("==", "equal to"),
	)

	student = models.ForeignKey(
		"usermgmt.Student",
		on_delete=models.CASCADE
	)

	# Current progress
	current = models.FloatField(default=0)

	# Target value and requirements
	target = models.FloatField()
	field = models.CharField(choices=FIELD_CHOICES, max_length=255)
	comparator = models.CharField(choices=COMPARITOR_CHOICES, default=">=", max_length=2)

	# Model settings
	model_name = models.CharField(choices=MODEL_NAME_CHOICES, max_length=255)
	filters = models.CharField(default="{}", max_length=255)

	# Status
	status = models.CharField(choices=STATUS_CHOICES, default="ongoing", max_length=255)

	# Time
	date = models.DateField(default=timezone.now) # Start date
	end_date = models.DateField(blank=True, null=True) # End date
	end_option = models.CharField(choices=END_OPTION_CHOICES, default="before", max_length=255)
	completion_date = models.DateField(blank=True, null=True)

	repeat = models.CharField(choices=REPEAT_CHOICES, default="once", max_length=255)
	cycle = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True)

	def get_records(self):
		data = [{
			"record": None,
			"goal": self,
			"value": self.current,
			"status": self.status,
			"cycle": self.cycle,
			"date":	self.completion_date,
		}]
		if not self.completion_date:
			data[0]["date"] = self.end_date if self.end_date else self.get_date_range()[1]

		qs = GoalRecord.objects.filter(goal=self)
		for item in qs:
			data.append({
				"record": item,
				"goal": self,
				"value": item.value,
				"status": item.status,
				"cycle": item.cycle,
				"date":	item.date,
			})
		return data

	def get_date_range(self):
		min_delta = relativedelta(weeks=self.cycle) if self.repeat == "weekly" else relativedelta(months=self.cycle)
		max_delta = relativedelta(weeks=1) if self.repeat == "weekly" else relativedelta(months=1)
		return (self.date + min_delta, self.date + max_delta)

	# Reset for the next cycle
	def reset(self):
		obj = GoalRecord.objects.create(
			goal = self,
			value = self.current,
			status = "fail" if self.status == "ongoing" else self.status,
			cycle = self.cycle,
		)
		
		if self.completion_date:
			obj.date = self.completion_date
			obj.save()

		self.current = 0
		self.cycle += 1
		self.status = "ongoing"
		self.completion_date = None
		self.save()

	def get_filter(self, name):
		filters = demjson3.decode(self.filters)
		return filters.get(name)

	# Return a verbose description of the goal e.g
	def verbose_filters(self):
		text = ""
		data = demjson3.decode(self.filters)
		for field, value in data.items():
			if text:
				text += ", "
			comparator = "==" if isinstance(value, str) else self.comparator
			text += f"{field} {comparator} {value}"
		return text
