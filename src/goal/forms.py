from django import forms
from django.utils import timezone
from .models import Goal

class EditorForm(forms.ModelForm):
	class Meta:
		model = Goal
		fields = ["target", "field", "comparator", "model_name", "filters", "date", "end_date", "end_option", "repeat"]

		widgets = {
			"target": forms.TextInput(attrs={
				"placeholder": "Numeric value",
			}),
			"date": forms.TextInput(attrs={
				"type": "date",
			"placeholder": "yyyy-mm-dd",
			}),
			"end_date": forms.TextInput(attrs={
				"type": "date",
				"placeholder": "yyyy-mm-dd",
			}),
		}


class CreditsTemplateForm(forms.ModelForm):
	NCEA_CHOICES = [
		("e", "E"),
		("m", "M"),
		("a", "A"),
	]

	ALPHABET_CHOICES = [
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

	grade = forms.ChoiceField(choices=())
	subject_code = forms.CharField(
		max_length = 255,
		required = False,
		widget = forms.TextInput(
			attrs={
				"placeholder":"Subject code",
				"autocomplete":"off",
			}
		),
	)
	year = forms.ChoiceField(choices=(), required=False)

	def __init__(self, student, *args, **kwargs):
		super(CreditsTemplateForm, self).__init__(*args, **kwargs)

		# Set year choices
		choices = [(None, "--")]
		current_year = timezone.now().date().year
		for i in range(current_year-5, current_year+5):
			choices.append((i, i))
		self.fields["year"].choices = choices

		# Set grade choices
		self.fields["grade"].choices = self.NCEA_CHOICES
		if student.grading_system == "alphabetical":
			self.fields["grade"].choices = self.ALPHABET_CHOICES
		self.fields["grade"].choices.append(("*", "All Passing Grade"))

	class Meta:
		model = Goal
		fields = ["target", "end_date"]
		widgets = {
			"target": forms.TextInput(
				attrs={
					"type": "number",
					"step": 1,
					"placeholder": "Credits",
				}
			),
			"end_date": forms.TextInput(attrs={
				"type": "date",
				"placeholder": "yyyy-mm-dd",
				"required": "true",
			}),
		}


class GPATemplateForm(forms.ModelForm):
	subject_code = forms.CharField(
		max_length = 255,
		required = False,
		widget = forms.TextInput(
			attrs={
				"placeholder":"Subject code",
				"autocomplete":"off",
			}
		),
	)
	year = forms.ChoiceField(choices=(), required=False)

	def __init__(self, student, *args, **kwargs):
		super(GPATemplateForm, self).__init__(*args, **kwargs)

		# Set year choices
		choices = [(None, "--")]
		current_year = timezone.now().date().year
		for i in range(current_year-5, current_year+5):
			choices.append((i, i))
		self.fields["year"].choices = choices

	class Meta:
		model = Goal
		fields = ["target", "end_date"]
		widgets = {
			"target": forms.TextInput(
				attrs={
					"type": "number",
					"step": 0.01,
					"placeholder": "GPA",
				}
			),
			"end_date": forms.TextInput(attrs={
				"type": "date",
				"placeholder": "yyyy-mm-dd",
				"required": "true",
			}),
		}


class RankScoreTemplateForm(forms.ModelForm):
	subject_code = forms.CharField(
		max_length = 255,
		required = False,
		widget = forms.TextInput(
			attrs={
				"placeholder":"Subject code",
				"autocomplete":"off",
			}
		),
	)

	class Meta:
		model = Goal
		fields = ["target", "end_date"]
		widgets = {
			"target": forms.TextInput(
				attrs={
					"type": "number",
					"step": 1,
					"placeholder": "Rank Score",
				}
			),
			"end_date": forms.TextInput(attrs={
				"type": "date",
				"placeholder": "yyyy-mm-dd",
				"required": "true",
			}),
		}


class FocusPeriodTemplateForm(forms.ModelForm):
	class Meta:
		model = Goal
		fields = ["target", "end_date", "repeat"]
		widgets = {
			"target": forms.TextInput(
				attrs={
					"type": "number",
					"step": 1,
					"placeholder": "Minutes",
				}
			),
			"end_date": forms.TextInput(attrs={
				"type": "date",
				"placeholder": "yyyy-mm-dd",
			}),
		}







