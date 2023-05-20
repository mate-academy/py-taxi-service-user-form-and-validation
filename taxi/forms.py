from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CleanLicenseNumberMixin:

    def clean_license_number(self) -> str:
        clean_license_number = self.cleaned_data["license_number"]

        if len(clean_license_number) != 8:
            raise ValidationError(
                "License numbers length should be 8 characters"
            )

        if not (
            clean_license_number[:3].isupper()
            and clean_license_number[:3].isalpha()
        ):
            raise ValidationError(
                "First 3 characters should be uppercase letters"
            )

        if not clean_license_number[3:].isnumeric():
            raise ValidationError("Last 5 characters should be digits")

        return clean_license_number


class DriverCreationForm(CleanLicenseNumberMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(CleanLicenseNumberMixin, forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
