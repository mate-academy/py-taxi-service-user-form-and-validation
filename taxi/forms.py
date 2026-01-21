from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Car

Driver = get_user_model()


class DriverLicenseUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Update license"))

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License must be exactly 8 characters long")
        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise ValidationError("First 3 characters must "
                                  "be uppercase letters")
        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits")
        return license_number

    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverCreationForm(UserCreationForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License must be exactly 8 characters long")
        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise ValidationError("First 3 characters "
                                  "must be uppercase letters")
        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits")
        return license_number

    class Meta:
        model = Driver
        fields = ["username", "first_name", "last_name", "license_number"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple
        }
