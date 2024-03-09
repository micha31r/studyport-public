from datetime import timedelta
from django.utils import timezone
from background_task import background
from background_task.models import Task
from .models import Verification


@background(schedule=0)
def remove_expired_verifications():
	limit = timezone.now() - timedelta(days=1)
	qs = Verification.objects.all()
	for obj in qs:
		if not obj.is_valid():
			obj.delete()


if not Task.objects.filter(verbose_name="remove_expired_verifications").exists():
	remove_expired_verifications(repeat=Task.DAILY, verbose_name="remove_expired_verifications", repeat_until=None)
