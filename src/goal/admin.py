from django.contrib import admin
from .models import Goal, GoalRecord

class GoalAdmin(admin.ModelAdmin):
    list_display = ("student", "verbose_filters", "status", "end_option", "repeat", "completion_date", "timestamp", "pk")
    search_fields = ("student__user__first_name", "student__user__last_name")
    readonly_fields = ["timestamp"]

class GoalRecordAdmin(admin.ModelAdmin):
    list_display = ("goal", "status", "date", "pk")
    search_fields = ("goal__student__user__first_name", "goal__student__user__last_name")

admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalRecord, GoalRecordAdmin)
