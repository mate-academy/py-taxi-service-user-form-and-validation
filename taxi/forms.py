from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator

from taxi.models import Driver


class DriverUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(
        required=True,
        validators=[
            MaxLengthValidator(8),
            MinLengthValidator(8),
        ]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if any(ch.isdigit() for ch in license_number[:3]) \
                or not license_number[:3].isupper():
            raise ValidationError(
                "The first three characters must be uppercase"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "The last five characters must be digits"
            )

        return license_number
