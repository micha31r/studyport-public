from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import StreakRecord, SubjectGPA, YearGPA


class StreakRecordAdmin(admin.ModelAdmin):
	list_display = ("student", "streak_type", "count", "datetime", "pk")
	search_fields = ("student",)


class SubjectGPAAdmin(admin.ModelAdmin):
	list_display = ("student", "playground", "subject", "datetime", "gpa", "pk")
	search_fields = ("student",)


class YearGPAAdmin(admin.ModelAdmin):
	list_display = ("student", "playground", "year", "datetime", "gpa", "pk")
	search_fields = ("student",)


admin.site.register(StreakRecord, StreakRecordAdmin)
admin.site.register(SubjectGPA, SubjectGPAAdmin)
admin.site.register(YearGPA, YearGPAAdmin)