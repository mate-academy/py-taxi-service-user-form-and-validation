from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberValidationMixin:
    LENGTH_LICENSE_NUMBER = 8

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LENGTH_LICENSE_NUMBER:
            raise ValidationError(
                "Length of license number must be 8 symbols!"
            )
        if (
            not license_number[:3].isalpha()
            or not license_number[:3].isupper()
            or not license_number[3:].isnumeric()

        ):
            raise ValidationError(
                "First three symbols must be uppercase letters "
                "and last 5 symbols must be numbers! "
                "Check your data again and repeat process."
            )
        return license_number


class DriverCreateForm(UserCreationForm, LicenseNumberValidationMixin):
    email = forms.EmailField(required=True, label="Email address")

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
