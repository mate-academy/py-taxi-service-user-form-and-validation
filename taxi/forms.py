from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(max_length=8)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",
                                                 "first_name",
                                                 "last_name",)

    def clean_license_number(self) -> str:
        license_number = (self.cleaned_data["license_number"])
        validation_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(max_length=8)

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self) -> str:
        license_number = (self.cleaned_data["license_number"])
        validation_license_number(license_number)
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


def validation_license_number(license_number: str) -> None:
    if len(license_number) != 8:
        raise ValidationError("License number must be 8 characters long")
    elif not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("The first 3 letters must be capitalized")
    elif not license_number[3:].isdigit():
        raise ValidationError("There should be 5 digits at the end")
