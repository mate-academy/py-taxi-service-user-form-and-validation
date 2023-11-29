from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    LICENSE_NUMBER_LENGTH = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != DriverCreationForm.LICENSE_NUMBER_LENGTH:
            raise ValidationError("Wrong license number")
        if license_number[:3] != license_number[:3].upper():
            raise ValidationError("Wrong license number")
        if not license_number[3:8].isdigit():
            raise ValidationError("Wrong license number")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != DriverCreationForm.LICENSE_NUMBER_LENGTH:
            raise ValidationError("Wrong license number")
        if license_number[:3] != license_number[:3].upper():
            raise ValidationError("Wrong license number")
        if not license_number[3:8].isdigit():
            raise ValidationError("Wrong license number")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
