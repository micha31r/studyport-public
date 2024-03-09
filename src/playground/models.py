from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.apps import apps


class Playground(models.Model):
	class Meta:
		ordering = ["student__user__last_name", "student__user__first_name", "-timestamp"]

	student = models.ForeignKey(
		"usermgmt.Student",
		on_delete = models.CASCADE,
	)

	name = models.CharField(default="New Playground", max_length=32)
	timestamp = models.DateTimeField(auto_now_add=True)

	def get_sources(self):
		Result = apps.get_model(app_label="results", model_name="Result")
		qs = Result.objects.filter(student=self.student, playground=self)
		items = []
		for obj in qs:
			if obj.play_source:
				items.append(obj.play_source)
		return items

	def get_source_ids(self):
		Result = apps.get_model(app_label="results", model_name="Result")
		qs = Result.objects.filter(student=self.student, playground=self)
		items = []
		for obj in qs:
			if obj.play_source:
				items.append(obj.play_source.id)
		return items

	def get_results(self):
		Result = apps.get_model(app_label="results", model_name="Result")
		qs = Result.objects.filter(student=self.student, playground=self)
		return qs

	def get_result_ids(self):
		Result = apps.get_model(app_label="results", model_name="Result")
		qs = Result.objects.filter(student=self.student, playground=self)
		items = []
		for obj in qs:
			items.append(obj.id)
		return items

	def delete(self, *args, **kwargs):
		if self.pk == self.student.recent_playground_id:
			self.student.recent_playground_id = None
		most_recent = Playground.objects.filter(student=self.student).order_by("pk").first()
		if most_recent:
			self.student.recent_playground_id = most_recent.pk
		self.student.save()
		super(Playground, self).delete(*args, **kwargs)

	# def get_results(self):
	# 	Result = apps.get_model(app_label="results", model_name="Result")
	# 	return Result.objects.filter(student=self.student, playground=self, reverse_play_source=None)

 