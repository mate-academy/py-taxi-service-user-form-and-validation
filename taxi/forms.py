from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
import re

from django.core.exceptions import ValidationError
from .models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.fullmatch(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "License number must consist of 3 "
                "uppercase letters followed by 5 digits."
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.fullmatch(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "License number must consist of 3 "
                "uppercase letters followed by 5 digits."
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Car
        fields = "__all__"
