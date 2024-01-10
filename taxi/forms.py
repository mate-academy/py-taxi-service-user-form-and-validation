from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarCreationForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self) -> None:
        license_number = self.cleaned_data["license_number"]
        print(license_number)
        literal = license_number[:3]
        digits = license_number[3:]
        if (
            literal != literal.upper()
            or not literal.isalpha()
            or not digits.isdigit()
            or len(license_number) != 8
        ):
            raise ValidationError("Invalid license number. Example: AAA12345")
        return license_number


class DriverCreateForm(
    UserCreationForm,
    DriverLicenseUpdateForm
):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "email"
        )
