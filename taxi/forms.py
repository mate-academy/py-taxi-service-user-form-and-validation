from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Driver


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        value = self.cleaned_data["license_number"]

        if len(value) != 8:
            raise forms.ValidationError(
                "The license plate must consist of 8 characters."
            )

        first = value[:3]
        last = value[3:]

        if not first.isalpha() or not first.isupper():
            raise forms.ValidationError(
                "The first 3 characters must be upper-case letters."
            )

        if not last.isdigit():
            raise forms.ValidationError(
                "The last 5 characters must be digits."
            )

        return value


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean_license_number(self):
        value = self.cleaned_data["license_number"]

        if len(value) != 8:
            raise forms.ValidationError(
                "The license plate must consist of 8 characters."
            )

        first = value[:3]
        last = value[3:]

        if not first.isalpha() or not first.isupper():
            raise forms.ValidationError(
                "The first 3 characters must be upper-case letters."
            )

        if not last.isdigit():
            raise forms.ValidationError(
                "The last 5 characters must be digits."
            )

        return value
