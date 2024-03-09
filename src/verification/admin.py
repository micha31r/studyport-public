from django.contrib import admin
from .models import Verification, AccountVerification

class VerificationAdmin(admin.ModelAdmin):
    list_display = ("label", "code", "duration", "timestamp", "pk")
    readonly_fields = ["timestamp"]


class AccountVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "verification", "pk")


admin.site.register(Verification, VerificationAdmin)
admin.site.register(AccountVerification, AccountVerificationAdmin)
