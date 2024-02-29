from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, RegexValidator

from taxi.models import Driver, Car


class DriversCreationForm(UserCreationForm):
    MAX_LENGTH_LICENSE = 8
    license_number = forms.CharField(
        required=True,
        validators=[
            MaxLengthValidator(MAX_LENGTH_LICENSE),
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License num: 3 uppercase letters + 5 digits"
            )
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            MaxLengthValidator(8),
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License num: 3 uppercase letters + 5 digits."
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return license_number
