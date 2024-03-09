from django.db import models
from django.utils import timezone


class FocusPeriod(models.Model):
	student = models.ForeignKey(
		"usermgmt.Student",
		on_delete=models.CASCADE
	)
	duration = models.DurationField()
	date = models.DateField(default=timezone.now)
	timestamp = models.DateTimeField(auto_now_add=True)

	def to_minutes(self):
		return self.duration.total_seconds() / 60