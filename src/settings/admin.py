from django.contrib import admin
from .models import ColorSettings

class ColorSettingsAdmin(admin.ModelAdmin):
    list_display = ('theme', 'student')

admin.site.register(ColorSettings, ColorSettingsAdmin)