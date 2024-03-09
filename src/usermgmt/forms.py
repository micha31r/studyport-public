from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder":"School Email Address"
            },
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Password"
            }
        )
    )