from django import forms
from usermgmt.models import Student
from .models import ColorSettings


class AppForm(forms.ModelForm):
    PROFILE_IMAGE_CHOICES = [
        ('jackalope', 'jackalope'), 
        ('rick-sanchez', 'rick-sanchez'), 
        ('peacock', 'peacock'), 
        ('babys-room', 'babys-room'), 
        ('owl', 'owl'), 
        ('stormtrooper', 'stormtrooper'), 
        ('butterfly', 'butterfly'), 
        ('account', 'account'), 
        ('orca', 'orca'), 
        ('panda', 'panda'), 
        ('toucan', 'toucan'), 
        ('shark', 'shark'), 
        ('baby-yoda', 'baby-yoda'), 
        ('flying-duck', 'flying-duck'), 
        ('bird', 'bird'), 
        ('finn', 'finn'), 
        ('kangaroo', 'kangaroo'), 
        ('octopus', 'octopus'), 
        ('flamingo', 'flamingo'), 
        ('leader', 'leader'), 
        ('quail', 'quail'), 
        ('lion', 'lion'), 
        ('pet-commands-summon', 'pet-commands-summon'), 
        ('giraffe-full-body', 'giraffe-full-body'), 
        ('turtle', 'turtle'), 
        ('unicorn', 'unicorn'), 
        ('batman', 'batman'), 
        ('whale', 'whale'), 
        ('horse', 'horse'), 
        ('happy', 'happy'), 
        ('parrot', 'parrot'), 
        ('fish', 'fish'), 
        ('snail', 'snail'), 
        ('phoenix', 'phoenix'), 
        ('snake', 'snake'), 
        ('monkey-with-a-banana', 'monkey-with-a-banana'), 
        ('pig', 'pig'), 
        ('budgie', 'budgie'), 
        ('puppy', 'puppy'), 
        ('kiwi-bird', 'kiwi-bird'), 
        ('fox', 'fox'), 
        ('seal', 'seal'), 
        ('bat', 'bat'), 
        ('teddy-bear', 'teddy-bear'), 
        ('snowman', 'snowman'), 
        ('jellyfish', 'jellyfish'), 
        ('hippopotamus', 'hippopotamus'), 
        ('dinosaur-egg', 'dinosaur-egg'), 
        ('person-female', 'person-female'), 
        ('frog-face', 'frog-face'), 
        ('santa', 'santa'), 
        ('cookie-monster', 'cookie-monster'), 
        ('cat', 'cat'), 
        ('puffin-bird', 'puffin-bird'), 
        ('sparrowhawk', 'sparrowhawk'), 
        ('iron-man', 'iron-man'), 
        ('watermelon', 'watermelon'), 
        ('cherry', 'cherry')
    ]
    profile_image = forms.ChoiceField(choices=PROFILE_IMAGE_CHOICES)

    class Meta:
        model = Student
        fields = ['year_level', 'viewing_year', 'show_mock_results']


class AccountForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder":"First Name"
            },
        )
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Last Name"
            },
        )
    )
    student_id = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Student ID"
            },
        )
    )
    email = forms.EmailField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Email"
            },
        )
    )


class PasswordForm(forms.Form):
    current_password = forms.CharField(
        required = False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Current Password",
                "autocomplete":"off"
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"New Password",
                "autocomplete":"off"
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Confirm Password",
                "autocomplete":"off"
            }
        )
    )

    def __init__(self, *args, **kwargs):
        has_password = kwargs["user"].has_usable_password()
        del kwargs["user"]
        super(PasswordForm, self).__init__(*args, **kwargs)
        if has_password:
            self.fields["current_password"].required = True


class NCEAThemeForm(forms.ModelForm):
    class Meta:
        model = ColorSettings
        fields = [
            'theme',
            'ncea_e',
            'ncea_m',
            'ncea_a',
            'ncea_na',
        ]
        labels = {
            "ncea_e": "E",
            "ncea_m": "M",
            "ncea_a": "A",
            "ncea_na": "NA",
        }


class AlphabetThemeForm(NCEAThemeForm):
    class Meta:
        model = ColorSettings
        fields = [
            'theme',
            'alphabet_a_plus',
            'alphabet_a',
            'alphabet_a_minus',
            'alphabet_b_plus',
            'alphabet_b',
            'alphabet_b_minus',
            'alphabet_c_plus',
            'alphabet_c',
            'alphabet_c_minus',
            'alphabet_d_plus',
            'alphabet_d',
            'alphabet_d_minus',
            'alphabet_f',
        ]
        labels = {
            'alphabet_a_plus':   'A+',
            'alphabet_a':        'A',
            'alphabet_a_minus':  'A-',
            'alphabet_b_plus':   'B+',
            'alphabet_b':        'B',
            'alphabet_b_minus':  'B-',
            'alphabet_c_plus':   'C+',
            'alphabet_c':        'C',
            'alphabet_c_minus':  'C-',
            'alphabet_d_plus':   'D+',
            'alphabet_d':        'D',
            'alphabet_d_minus':  'D-',
            'alphabet_f':        'F',
        }



