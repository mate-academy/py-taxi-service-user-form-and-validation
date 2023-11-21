from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django import forms

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(regex="^[A-Z]{3}\\d{5}$",
                           message=("License number must be of length 8,"
                                    " start with 3 uppercase letters"
                                    " and end with 5 digits"))
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(regex="^[A-Z]{3}\\d{5}$",
                           message=("License number must be of length 8,"
                                    " start with 3 uppercase letters"
                                    " and end with 5 digits"))
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)
