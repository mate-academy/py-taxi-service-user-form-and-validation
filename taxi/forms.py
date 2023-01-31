from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator  # noqa: E501

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LENGTH = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError(
                f"License number length have to be equal {self.LICENSE_LENGTH}"
            )

        if license_number[:3].isdigit() or not license_number[:3].isupper():
            raise ValidationError(
                "First three elements have to be letters and uppercase"
            )

        if not license_number[4:].isdigit():
            raise ValidationError(
                "After third element all elements have to be digits"
            )
        return license_number


class DriverForm(UserCreationForm):
    LICENSE_LENGTH = 8
    MESSAGE = "License number have first 3 uppercase letters than 5 numbers!"
    REGEX = "[A-Z]{3}[0-9]{5}"

    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(LICENSE_LENGTH),
            MaxLengthValidator(LICENSE_LENGTH),
            RegexValidator(
                message=MESSAGE,
                regex=REGEX
            )
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )
