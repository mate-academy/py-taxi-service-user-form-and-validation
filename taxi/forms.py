from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


class BaseDriverForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Invalid license number! Length must be 8 characters."
            )
        if not license_number[0:3].isalpha():
            raise ValidationError(
                "Invalid license number!"
                " First 3 characters must contain only letters."
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "Invalid license number!"
                " Last 5 characters must contain only digits."
            )
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


class DriverForm(BaseDriverForm):

    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "license_number",
            "password"
        )


class DriverLicenseUpdateForm(BaseDriverForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
