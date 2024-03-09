from django.apps import apps
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.http import Http404
from django.core.validators import MaxValueValidator, MinValueValidator
from settings.models import ColorSettings
from standards.models import Subject, Assessment
from verification.models import Verification
from results.utils import get_results

User = settings.AUTH_USER_MODEL

def get_year():
	return timezone.now().year


class Student(models.Model):
	class Meta:
		ordering = ["user__last_name", "user__first_name"]
		
	YEAR_LEVEL_CHOICES = (
	    (9, "Year 9"),
	    (10, "Year 10"),
	    (11, "Year 11"),
	    (12, "Year 12"),
	    (13, "Year 13"),
	)

	GRADING_CHOICES = (
		# NA, A, M, E
	    ("ncea", "NCEA"),
	    # A+, A, A-, B+, B, B- ...
	    ("alphabetical", "Alphabetical"),
	)

	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE
	)

	profile_image = models.CharField(default="account", max_length=255)

	school = models.ForeignKey(
		"group.School",
		on_delete = models.SET_NULL,
		blank=True,
		null=True,
	)

	color_settings = models.OneToOneField(
		"settings.ColorSettings",
		null=True,
		on_delete = models.SET_NULL,
	)

	student_id = models.IntegerField()
	year_level = models.IntegerField(default=9, choices=YEAR_LEVEL_CHOICES)
	viewing_year = models.IntegerField(default=get_year)
	show_mock_results = models.BooleanField(default=False)
	recent_playground_id = models.IntegerField(blank=True, null=True)
	playground_is_active = models.BooleanField(default=False)
	internal_weighting = models.FloatField(default=1)
	external_weighting = models.FloatField(default=1)
	grading_system = models.CharField(default="ncea", max_length=16, choices=GRADING_CHOICES)
	is_verified = models.BooleanField(default=False)
	starting_date = models.DateField(default=timezone.now)
	is_active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def get_unique_id(self):
		return ("%06d" % self.school.moe_code) + ("%014d" % self.student_id)

	def get_highest_streak(self, streak_type):
		StreakRecord = apps.get_model("stats.StreakRecord")
		return StreakRecord.objects.filter(streak_type=streak_type).order_by("-count").first()

	def get_current_focus_period(self):
		FocusPeriod = apps.get_model("focus.FocusPeriod")
		return FocusPeriod.objects.filter(student=self, date=timezone.now()).first()

	def get_profile_url(self):
		return f"/static/icons8/profile/{self.profile_image}.svg"

	def to_year(self, year_level):
		return self.starting_date.year + year_level - 9

	def to_year_level(self, year):
		return year - self.starting_date.year + 9

	def get_subjects(self, year=None, year_level=None, include_empty=False):
		qs = get_results(self, date__year=year, include_empty=include_empty) if year else get_results(self, assessment__level=year_level-10, include_empty=include_empty)
		subject_pks = qs.values_list("subject").distinct()
		return Subject.objects.filter(pk__in=subject_pks)

	def get_weighting(self, assessment_type):
		return self.internal_weighting if assessment_type == "i" else self.external_weighting

	def get_playground(self):
		Playground = apps.get_model("playground.Playground")
		if not self.recent_playground_id:
			obj = Playground.objects.filter(student=self).order_by("pk").first()
			if obj:
				self.recent_playground_id = obj.pk
				self.save()
		return Playground.objects.filter(student=self, pk=self.recent_playground_id).first()

	def activate_playground(self):
		obj = self.get_playground()
		if obj:
			self.playground_is_active = True
			self.save()
			return True
		return False

	def deactivate_playground(self):
		obj = self.get_playground()
		self.playground_is_active = False
		self.save()
		return True

	def save(self, *args, **kwargs):
		if not self.color_settings:
			self.color_settings = ColorSettings.objects.create()
		super(Student, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		if self.profile_image:
			self.profile_image.delete()
		super(Student, self).delete(*args, **kwargs)

	def __str__(self):
		return self.user.get_full_name()
