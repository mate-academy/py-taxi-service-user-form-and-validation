from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from taxi.models import Driver, Car

class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License must be 3 "
                        "uppercase letters followed by 5 digits"
            )
        ],
        help_text="Format: 3 uppercase letters + 5 digits (e.g., ABC12345)"
    )
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )

class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License must be 3 uppercase"
                        " letters followed by 5 digits"
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple
        }
