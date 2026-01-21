import re

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes import forms
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        return (
            self.validate_license_number(
                self.cleaned_data.get("license_number")
            )
        )

    @classmethod
    def validate_license_number(cls, license_number):
        if not license_number:
            raise ValidationError(gettext_lazy("This field is required."))

        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                gettext_lazy(
                    "Enter a valid license number in the format ABC12345."
                )
            )

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return (
            DriverCreationForm
            .validate_license_number(self.cleaned_data.get("license_number"))
        )


class CarForm(forms.ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
