from django.db.models.signals import post_save
from .models import FocusPeriod
from .handlers import *

post_save.connect(focus_streak_handler, sender=FocusPeriod)
