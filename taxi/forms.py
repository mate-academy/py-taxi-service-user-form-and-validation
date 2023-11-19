from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.Form):
    license_number = forms.CharField(
        label='Driver\'s License Number',
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}\d{5}$',
                message='The driver\'s license must consist of 3 uppercase letters followed by 5 digits.',
            ),
        ],
        widget=forms.TextInput(attrs={'placeholder': 'ABC12345'}),
    )
