from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import CheckboxSelectMultiple

from taxi.models import Driver, Car


def license_number_validator(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError("Invalid license length")
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise forms.ValidationError("First 3 character "
                                    "must be uppercase letters")
    if not license_number[3:].isdigit():
        raise forms.ValidationError("Last 5 character must be digits")

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return license_number_validator(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return license_number_validator(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
