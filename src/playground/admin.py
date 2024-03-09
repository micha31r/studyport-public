from django.contrib import admin
from .models import Playground

class PlaygroundAdmin(admin.ModelAdmin):
    list_display = ("name", "student", "timestamp", "pk")
    search_fields = ("student__user__first_name", "student__user__last_name")
    readonly_fields = ["timestamp"]

admin.site.register(Playground, PlaygroundAdmin)
