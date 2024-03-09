from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from .conversion import name_to_abbv, abbv_to_name
	

class Result(models.Model):
	class Meta:
		ordering = ["assessment__title"]

	student = models.ForeignKey(
		"usermgmt.Student",
		on_delete=models.CASCADE
	)

	playground = models.ForeignKey(
		"playground.Playground",
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)

	subject = models.ForeignKey(
		"standards.Subject",
		on_delete=models.CASCADE
	)

	assessment = models.ForeignKey(
		"standards.Assessment",
		on_delete=models.CASCADE
	)

	play_source = models.OneToOneField(
		"self",
		related_name="reverse_play_source",
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)

	grade = models.CharField(max_length=255, blank=True, null=True)
	is_mock = models.BooleanField(default=False)
	is_published = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	date = models.DateField(default=timezone.now)

	def name_to_abbv(self):
		if self.student.grading_system == "ncea":
			return name_to_abbv(self.grade)
		return self.grade

	def abbv_to_name(self):
		if self.student.grading_system == "ncea":
			return abbv_to_name(self.grade)
		return self.grade

	def is_original(self):
		if not self.playground:
			return True

	def save(self, *args, **kwargs):
		if self.student.playground_is_active:
			if self.pk: 
				if self.is_original():
					alias = getattr(self, "reverse_play_source", None)
					if alias:
						# Update existing alias
						alias.subject = self.subject
						alias.assessment = self.assessment
						alias.grade = self.grade
						alias.is_mock = self.is_mock
						alias.date = self.date
						alias.save()
					else:
						# Cache new values
						playground = self.student.get_playground()
						subject = self.subject
						assessment = self.assessment
						play_source = self
						grade = self.grade
						is_mock = self.is_mock
						date = self.date
						
						# Reset current object to original values
						og = Result.objects.get(pk=self.pk)
						self.subject = og.subject
						self.assessment = og.assessment
						self.grade = og.grade
						self.is_mock = og.is_mock
						self.date = og.date

						# Create alias object based on cached values
						Result.objects.create(
							student = self.student,
							playground = playground,
							subject = subject,
							assessment = assessment,
							play_source = play_source,
							grade = grade,
							is_mock = is_mock,
							date = date,
						)
					return
			else:
				self.playground = self.student.get_playground()
		super(Result, self).save(*args, **kwargs)


