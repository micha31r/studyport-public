from django.db import models
from django.utils import timezone


def get_year():
	return timezone.now().year


class StreakRecord(models.Model):
	class Meta:
		ordering = ["student", "streak_type", "count", "-datetime"]

	STREAK_TYPE_CHOICES = (
		("goal", "Goal"),
		("focus", "Focus")
	)

	student = models.ForeignKey(
		"usermgmt.Student",
		on_delete = models.CASCADE
	)
	streak_type = models.CharField(choices=STREAK_TYPE_CHOICES, max_length=16)
	datetime = models.DateTimeField(default=timezone.now)
	count = models.IntegerField()


class SubjectGPA(models.Model):
	class Meta:
		ordering = ["student", "subject", "-datetime"]

	student = models.ForeignKey(
		"usermgmt.Student",
		on_delete = models.CASCADE
	)
	subject = models.ForeignKey(
		"standards.Subject",
		on_delete = models.CASCADE,
		null = True,
		blank = True,
	)
	playground = models.ForeignKey(
		"playground.Playground",
		on_delete = models.CASCADE,
		blank = True,
		null = True,
	)
	datetime = models.DateTimeField(default=timezone.now)
	gpa = models.FloatField()
	mock_gpa = models.FloatField()

	def get_gpa(self):
		if self.student.show_mock_results:
			return self.mock_gpa
		return self.gpa


class YearGPA(models.Model):
	class Meta:
		ordering = ["student", "year", "-datetime"]

	student = models.ForeignKey(
		"usermgmt.Student",
		on_delete=models.CASCADE
	)
	playground = models.ForeignKey(
		"playground.Playground",
		on_delete = models.CASCADE,
		blank = True,
		null = True,
	)
	datetime = models.DateTimeField(default=timezone.now)
	year = models.IntegerField(default=get_year)
	gpa = models.FloatField()
	mock_gpa = models.FloatField()

	def get_gpa(self):
		if self.student.show_mock_results:
			return self.mock_gpa
		return self.gpa
