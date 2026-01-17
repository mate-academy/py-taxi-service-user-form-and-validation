from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


def clean_license(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "License number should contain 8 characters."
        )
    if not (license_number[:3].isalpha() and license_number[:3].isupper()):
        raise ValidationError(
            "The first 3 characters should be letters and uppercase."
        )
    if not license_number[3:].isdigit():
        raise ValidationError(
            "The last 5 characters should be numbers."
        )
    return license_number


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        return clean_license(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return clean_license(self.cleaned_data["license_number"])


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
