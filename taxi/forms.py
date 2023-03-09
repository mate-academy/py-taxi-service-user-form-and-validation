from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    min_license_number_length = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) \
                != DriverLicenseUpdateForm.min_license_number_length:
            raise ValidationError(
                "License number should have at least "
                f"{DriverLicenseUpdateForm.min_license_number_length} letters"
            )

        if (
                not license_number[:3].isalpha()
                or license_number[:3] != license_number[:3].upper()
        ):
            raise ValidationError(
                "First 3 characters have to be uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters have to be digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
