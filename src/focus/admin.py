from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import FocusPeriod


class FocusPeriodAdmin(admin.ModelAdmin):
	list_display = ("student", "duration", "date", "timestamp", "pk")
	search_fields = ("student",)
	readonly_fields = ["timestamp"]
	

admin.site.register(FocusPeriod, FocusPeriodAdmin)