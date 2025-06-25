from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Driver, Car
import re


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            raise forms.ValidationError("To pole jest wymagane.")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "Numer prawa jazdy musi mieć dokładnie 8 znaków.")

        if not re.match(r"^[A-Z]{3}[0-9]{5}$",
                        license_number):
            raise forms.ValidationError(
                "Numer musi zaczynać się od 3"
                " wielkich liter i kończyć 5 cyframi.")

        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ("username",
                  "license_number",
                  "email")

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            raise forms.ValidationError("To pole jest wymagane.")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "Numer prawa jazdy musi mieć dokładnie 8 znaków.")

        if not re.match(r"^[A-Z]{3}[0-9]{5}$", license_number):
            raise forms.ValidationError(
                "Numer musi zaczynać się od 3 wielkich"
                " liter i kończyć 5 cyframi.")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Car
        fields = "__all__"
