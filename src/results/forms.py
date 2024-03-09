from django import forms
from django.utils import timezone


class FilterForm(forms.Form):
	wildcard = forms.CharField(
		required = False,
		max_length = 255,
		widget = forms.TextInput(
			attrs={
				"placeholder":"Search fields",
			}
		),
	)
	year = forms.ChoiceField(choices=(), required=False)

	def __init__(self, student, *args, **kwargs):
		super(FilterForm, self).__init__(*args, **kwargs)

		# Set year choices
		choices = [(None, "All Years")]
		for i in range(student.starting_date.year, timezone.now().date().year):
			choices.append((i, i))
		self.fields["year"].choices = choices


class NCEAEditForm(forms.Form):
	GRADE_CHOICES = (
		(None, "--"),
		("e", "E"),
		("m", "M"),
		("a", "A"),
		("na", "NA"),
	)

	subject_code = forms.CharField(
		max_length=255,
		widget=forms.TextInput(
			attrs={
				"placeholder":"Subject code",
				"autocomplete":"off",
			}
		),
	)
	assessment_code = forms.CharField(
		max_length=255,
		widget=forms.TextInput(
			attrs={
				"placeholder":"Assessment code",
				"autocomplete":"off",
			}
		),
	)
	date 	= forms.DateTimeField(
		widget=forms.TextInput(
			attrs={
				"type":"date",
				"placeholder":"yyyy-mm-dd"
			}
		),
		required=False
	)
	grade 			= forms.CharField(widget=forms.Select(choices=GRADE_CHOICES), required=False)
	is_mock 		= forms.BooleanField(required=False)
	is_published 	= forms.BooleanField(required=False)
	

class AlphabetEditForm(NCEAEditForm):
	GRADE_CHOICES = [
		(None, "--"),
		("a+", "A+"),
		("a", "A"),
		("a-", "A-"),
		("b+", "B+"),
		("b", "B"),
		("b-", "B-"),
		("c+", "C+"),
		("c", "C"),
		("c-", "C-"),
		("d+", "D+"),
		("d", "D"),
		("d-", "D-"),
		("f", "F"),
	]

	grade = forms.CharField(widget=forms.Select(choices=GRADE_CHOICES), required=False)