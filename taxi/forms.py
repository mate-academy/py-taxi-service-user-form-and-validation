from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_ = self.cleaned_data["license_number"]

        if len(license_) != 8:
            raise ValidationError(
                "License must be exactly 8 characters long."
            )

        prefix = license_[:3]
        suffix = license_[3:]

        if not prefix.isalpha() or not prefix.isupper():
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not suffix.isdigit():
            raise ValidationError(
                "Last 5 characters must be digits."
            )

        return license_


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number"))

    def clean_license_number(self):
        license_ = self.cleaned_data["license_number"]

        if len(license_) != 8:
            raise ValidationError("License must be exactly 8 characters long.")

        prefix = license_[:3]
        suffix = license_[3:]

        if not prefix.isalpha() or not prefix.isupper():
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not suffix.isdigit():
            raise ValidationError("Last 5 characters must be digits.")

        return license_


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
