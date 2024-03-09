from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .utils import random_string


User = settings.AUTH_USER_MODEL


class Verification(models.Model):
	class Meta:
		ordering = ["-timestamp"]

	label = models.CharField(blank=True, null=True, max_length=255)
	code = models.CharField(blank=True, max_length=6)
	duration = models.IntegerField(default=3600, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def is_valid(self):
		if not self.duration or timezone.now() < self.timestamp + timedelta(seconds=self.duration):
			return True
		return False

	def save(self, *args, **kwargs):
		if not self.code:
			self.code = random_string(size=6)
		super(Verification, self).save(*args, **kwargs)


class AccountVerification(models.Model):
	class Meta:
		ordering = ["-verification__timestamp"]

	user = models.OneToOneField(
		User,
		on_delete = models.CASCADE
	)

	verification = models.OneToOneField(
		"verification.Verification",
		on_delete = models.CASCADE,
		blank = True,
		null = True
	)

	def save(self, *args, **kwargs):
		if not self.verification:
			self.verification = Verification.objects.create(label="account verification")
		super(AccountVerification, self).save(*args, **kwargs)






