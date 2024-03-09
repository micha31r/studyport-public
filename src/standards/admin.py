from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import Assessment, Subject


class SubjectAdmin(admin.ModelAdmin):
	list_display = ("subject_code", "name", "department", "qualification", "year_level", "immutable", "pk")
	search_fields = ("subject_code", "name", "department")


class AssessmentAdmin(admin.ModelAdmin):
	list_display = ("assessment_code", "title", "credits", "level", "assessment_type", "immutable", "pk")
	search_fields = ("assessment_code", "title")


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Assessment, AssessmentAdmin)