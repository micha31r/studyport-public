from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "student_id", "school", "timestamp", "pk")
    search_fields = ("user__first_name", "user__last_name")
    readonly_fields = ["timestamp"]

    def first_name(self, obj):
    	return obj.user.first_name

    def last_name(self, obj):
    	return obj.user.last_name


admin.site.register(Student, StudentAdmin)
