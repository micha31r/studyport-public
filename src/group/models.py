import string, random, os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from verification.models import Verification


class School(models.Model):
	class Meta:
		ordering = ["name"]

	name = models.CharField(max_length=128, unique=True)
	slug = models.SlugField(blank=True, null=True, unique=True)
	moe_code = models.CharField(blank=True, null=True, unique=True, max_length=5)
	#email_domain
	web_domain = models.CharField(max_length=128, default="")
	completed_first_full_sync = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)

