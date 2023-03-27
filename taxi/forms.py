from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)
        license_number = forms.CharField(min_length=8)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError(
                f"Ensure that license number contains {self.LICENSE_LENGTH}"
            )

        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError("First three characters must be capitalize")

        if not license_number[3:].isdigit():
            raise ValidationError("Last five characters must be digits")

        return license_number
