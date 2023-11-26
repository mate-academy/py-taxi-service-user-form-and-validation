from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Driver, Car


def validate_license_number(license_number: str):
    def starts_with_three_uppercase_letters(string: str):
        starts_with = string[:3]
        return starts_with.isalpha() and starts_with.isupper()

    def ends_with_five_numbers(string: str):
        ends_with = string[3:]
        return ends_with.isdigit()

    if len(license_number) != 8:
        raise ValidationError(
            "License number should be 8 characters long!"
        )

    if not starts_with_three_uppercase_letters(license_number):
        raise ValidationError(
            "License number should start with 3 uppercase letters!"
        )

    if not ends_with_five_numbers(license_number):
        raise ValidationError(
            "License number should end with 5 numbers!"
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
