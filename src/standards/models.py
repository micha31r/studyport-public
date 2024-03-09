from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
	YEAR_LEVEL_CHOICES = (
	    (9, "Year 9"),
	    (10, "Year 10"),
	    (11, "Year 11"),
	    (12, "Year 12"),
	    (13, "Year 13"),
	)
	
	subject_code = models.CharField(max_length=8)
	name = models.CharField(max_length=128)
	department = models.CharField(max_length=128)
	qualification = models.CharField(max_length=128, blank=True, null=True)
	year_level = models.IntegerField(default=9, choices=YEAR_LEVEL_CHOICES)
	immutable = models.BooleanField(default=True)

	def __str__(self):
		return self.subject_code


class Assessment(models.Model):
	ASSESSMENT_TYPE_CHOICES = (
	    ("i", "Internal"),
	    ("e", "External"),
	)

	LEVEL_CHOICES = (
	    (1, "Level 1"),
	    (2, "Level 2"),
	    (3, "Level 3"),
	    (4, "Level 4"),
	    (5, "Level 5"),
	)

	assessment_code = models.CharField(max_length=255)
	"""
	A = Achievement standard
	U = Unit standard
	G = Internally assessed
	X = Learning recongnition
	S = Report card
	"""
	result_type = models.CharField(max_length=1)
	title = models.CharField(max_length=255)
	subfield = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	credits = models.IntegerField()
	level = models.IntegerField(default=1, choices=LEVEL_CHOICES)
	assessment_type = models.CharField(default="i", choices=ASSESSMENT_TYPE_CHOICES, max_length=1)
	immutable = models.BooleanField(default=True)

	def get_year_level(self):
		return self.level + 10

	def __str__(self):
		return self.assessment_code
