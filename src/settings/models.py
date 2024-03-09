from django.db import models
from colorfield.fields import ColorField
from .themes import CHART_PALETTE

class ColorSettings(models.Model):
	THEME_CHOICES = (
	    ("blue", 'Blue'),
	    ("red", 'Red'),
	    ("yellow", 'Yellow'),
	    ("purple", 'Purple'),
	    ("green", 'Green'),
	)

	COLOR_CHOICES = (
	    (CHART_PALETTE[0], "Light blue"),
	    (CHART_PALETTE[1], "Dark blue"),
	    (CHART_PALETTE[2], "Pink"),
	    (CHART_PALETTE[3], "Light purple"),
	    (CHART_PALETTE[4], "Turquoise"),
	    (CHART_PALETTE[5], "Bright pink"),
	    (CHART_PALETTE[6], "Orange"),
	    (CHART_PALETTE[7], "Light orange"),
	    (CHART_PALETTE[8], "Yellow"),
	    (CHART_PALETTE[9], "Dark green"),
	    (CHART_PALETTE[10], "Blue"),
	    (CHART_PALETTE[11], "Light yellow"),
	    (CHART_PALETTE[12], "Red"),
	    (CHART_PALETTE[13], "Purple"),
	    (CHART_PALETTE[14], "Light green"),
	)

	theme = models.CharField(default="blue", choices=THEME_CHOICES, max_length=16)

	# NCEA
	ncea_e = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[1])
	ncea_m = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[0])
	ncea_a = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[2])
	ncea_na = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[5])

	# Alphabetical
	alphabet_a_plus = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[0])
	alphabet_a = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[1])
	alphabet_a_minus = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[2])

	alphabet_b_plus = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[3])
	alphabet_b = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[4])
	alphabet_b_minus = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[5])

	alphabet_c_plus = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[6])
	alphabet_c = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[7])
	alphabet_c_minus = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[8])

	alphabet_d_plus = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[9])
	alphabet_d = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[10])
	alphabet_d_minus = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[11])

	alphabet_f = ColorField(choices=COLOR_CHOICES, default=CHART_PALETTE[12])

