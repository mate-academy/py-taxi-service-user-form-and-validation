from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


def license_number_validation(license_number: str) -> str:
    if len(license_number) != 8:
        raise forms.ValidationError("License must be 8 characters long")
    if not license_number[:3].isalpha():
        raise forms.ValidationError("First 3 characters must be letters")
    if not license_number[:3].isupper():
        raise forms.ValidationError("First 3 letters must be uppercase")
    if not license_number[3:].isnumeric():
        raise forms.ValidationError("last 5 characters must be numeric")
    return license_number


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self) -> str:
        return license_number_validation(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return license_number_validation(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
