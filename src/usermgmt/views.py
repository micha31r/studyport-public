import datetime, uuid
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import FormView
from django.http import Http404
from django.urls import reverse
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2View, OAuth2CallbackView
from allauth.socialaccount.providers.base.constants import AuthAction
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.helpers import render_authentication_error
from verification.models import AccountVerification
from settings.models import ColorSettings
from group.models import School
from notifications.models import Notification
from .decorators import user_has_access
from .models import Student
from .forms import *
from .mixins import CustomOAuthLoginMixin


class CustomOAuth2LoginView(CustomOAuthLoginMixin, OAuth2View):
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			# print(list(messages.get_messages(request)))
			return redirect("stats:overview")
		return super(CustomOAuth2LoginView, self).dispatch(request, *args, **kwargs)

	def login(self, request, *args, **kwargs):
		provider = self.adapter.get_provider()
		app = provider.get_app(self.request)
		client = self.get_client(request, app)
		action = request.GET.get("action", AuthAction.AUTHENTICATE)
		auth_url = self.adapter.authorize_url
		auth_params = provider.get_auth_params(request, action)
		client.state = SocialLogin.stash_state(request)
		try:
			return HttpResponseRedirect(client.get_redirect_url(auth_url, auth_params))
		except OAuth2Error as e:
			return render_authentication_error(request, provider.id, exception=e)


custom_oauth2_login = CustomOAuth2LoginView.adapter_view(GoogleOAuth2Adapter)


class CustomOAuth2CallbackView(OAuth2CallbackView):
	def dispatch(self, request, *args, **kwargs):
		response = super(CustomOAuth2CallbackView, self).dispatch(request, *args, **kwargs)
		if User.objects.get(pk=request.user.pk).is_authenticated:
			# Clear messages
			list(messages.get_messages(request))
			return redirect("usermgmt:account-migration")
		else:
			# Login failed
			pass
		return response


custom_oauth2_callback = CustomOAuth2CallbackView.adapter_view(GoogleOAuth2Adapter)


def password_login_view(request):
	ctx = {}
	next_page = request.GET.get("next")

	if request.user.is_authenticated:
		return redirect(next_page or "stats:overview")

	if request.POST:
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(request, username=username, password=password)
			
			if user:
				login(request, user)
				return redirect(next_page or "stats:overview")
			messages.error(request, "Incorrect email or password")
	
	ctx["form"] = LoginForm()
	return render(request, "usermgmt/login.html", ctx)


@login_required
def account_migration_view(request):
	"""
	Connect to synced account
	Synced users have empty email fields and are set to inactive
	"""
	synced_user = User.objects.filter(username=request.user.email, email__in=["", None], is_active=False).first()

	if synced_user:
		pass
		if request.user.socialaccount_set.count() > 0:
			social_acount = request.user.socialaccount_set.all()[0]
			email_address_obj = request.user.emailaddress_set.all()[0]
			
			# Set synced user as main user and delete the recently created user
			social_acount.user = synced_user
			email_address_obj.user = synced_user
			social_acount.save()
			email_address_obj.save()
			request.user.delete()

			synced_user.is_active = True
			synced_user.email = synced_user.username
			synced_user.save()

			# https://stackoverflow.com/questions/64235399/django-why-do-i-need-to-specify-the-user-backend-when-logging-in-with-a-custom
			synced_user.backend = "django.contrib.auth.backends.ModelBackend"
			login(request, synced_user)

	else:
		if not Student.objects.filter(user=request.user).exists():
			request.user.username = request.user.email
			request.user.save()

			# Set up student profile
			school = School.objects.filter(web_domain=request.user.email.split("@")[:-1]).first()
			if school:
				profile = Student.objects.create(
					user = request.user,
					school = school,
				)
				profile.save()
			else:
				messages.error(request, "Login failed. Your google account is not link to any schools using Studyport")
				request.user.delete()

	return redirect(request.GET.get("next") or "stats:overview")


@login_required
def logout_view(request):
	logout(request)
	return redirect("usermgmt:login")



