from django.shortcuts import render
from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.base.mixins import OAuthLoginMixin


class CustomOAuthLoginMixin(OAuthLoginMixin):
    def dispatch(self, request, *args, **kwargs):
        provider = self.adapter.get_provider()
        if (not app_settings.LOGIN_ON_GET) and request.method == "GET":
            return render(
                request,
                "usermgmt/login.html",
                {
                    "provider": provider,
                    "process": request.GET.get("process"),
                },
            )
        return self.login(request, *args, **kwargs)