from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm

from taxi.models import Driver, Car


def validate_license_number(data):
    if not len(data) == 8:
        raise ValidationError(
            "License number must consist only of 8 characters"
        )

    if (
            not data[:3].isalpha()
            or not data[:3].isupper()
    ):
        raise ValidationError(
            "First 3 characters must be uppercase letters"
        )
    if not data[-5:].isdigit():
        raise ValidationError("Last 5 characters must be digits")


class LicenseNumberMixin:

    def clean_license_number(self):
        data = self.cleaned_data.get("license_number")
        if data:
            validate_license_number(data)
        return data


class DriverLicenseUpdateForm(LicenseNumberMixin, ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(LicenseNumberMixin, UserCreationForm):
    driver_license_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=get_user_model().objects.all(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
