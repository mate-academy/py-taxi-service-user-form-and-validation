from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car
import re


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "License must consist of 8 characters: "
                "first 3 uppercase letters, followed by 5 digits."
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number", "is_staff")