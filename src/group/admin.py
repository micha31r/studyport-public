from django.contrib import admin
from django.shortcuts import get_object_or_404
import usermgmt.models
from .models import School 


class SchoolAdmin(admin.ModelAdmin):
	list_display = ("name", "web_domain", "completed_first_full_sync", "timestamp", "pk")
	search_fields = ("name",)
	readonly_fields = ["timestamp"]


admin.site.register(School, SchoolAdmin)

