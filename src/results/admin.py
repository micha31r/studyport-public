from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import Result


class ResultAdmin(admin.ModelAdmin):
	list_display = ("assessment", "student", "credits", "grade", "date", "timestamp", "pk")
	search_fields = ("assessment",)
	readonly_fields = ["timestamp"]

	def credits(self, instance):
		return instance.assessment.credits


admin.site.register(Result, ResultAdmin)