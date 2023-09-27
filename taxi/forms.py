from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def clean_license_number(cleaned_data):
    license_number_length = 8
    license_number = cleaned_data["license_number"]
    if len(license_number) != license_number_length:
        raise ValidationError(
            "The license number should be "
            f"{license_number_length} characters long"
        )
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("First 3 symbols should be capital letters")
    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 symbols should be numbers")
    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )

    def clean(self):
        clean_license_number(self.cleaned_data)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean(self):
        clean_license_number(self.cleaned_data)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
