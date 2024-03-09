from django import forms
from .models import Playground

class EditForm(forms.ModelForm):
	class Meta:
		model = Playground
		fields = ["name"]

		widgets = {
			"name": forms.TextInput(attrs={
				"placeholder": "Name"
			}),
		}
	