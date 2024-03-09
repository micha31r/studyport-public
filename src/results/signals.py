from django.db.models.signals import post_save, post_delete
from results.models import Result
from .handlers import *

post_save.connect(gpa_handler, sender=Result)
post_delete.connect(gpa_handler, sender=Result)
