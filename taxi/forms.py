from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Driver, Car, Manufacturer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
import re


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        required=True,
        help_text="Required format: 3 uppercase letters, "
                  "5 numbers (e.g. ABC12345)"
    )
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if license_number:
            if not re.fullmatch(r"^[A-Z]{3}\d{5}$", license_number):
                raise forms.ValidationError(
                    "The license number must consist "
                    "of 3 capital letters and 5 digits."
                )
            if Driver.objects.filter(license_number=license_number).exists():
                raise forms.ValidationError("A driver's license with "
                                            "this number already exists.")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "license_number",
            Submit("submit", "Update license",
                   css_class="btn btn-success mt-3")
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if license_number:
            if not re.fullmatch(r"^[A-Z]{3}\d{5}$", license_number):
                raise forms.ValidationError(
                    "The license number must consist of "
                    "3 capital letters and 5 digits."
                )
            if Driver.objects.filter(license_number=license_number).exclude(
                    pk=self.instance.pk
            ).exists():
                raise forms.ValidationError("A driver's license with "
                                            "this number already exists.")
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "model",
            "manufacturer",
            "drivers",
            Submit("submit", "Save the car",
                   css_class="btn btn-primary mt-3")
        )


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["username", "first_name",
                  "last_name", "email", "license_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["username", "first_name", "last_name", "email"]:
            self.fields[field_name].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "username",
            "first_name",
            "last_name",
            "email",
            "license_number",
            Submit("submit", "Save changes", css_class="btn btn-primary mt-3")
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if license_number:
            if not re.fullmatch(r"^[A-Z]{3}\d{5}$", license_number):
                raise forms.ValidationError(
                    "The license number must consist of "
                    "3 capital letters and 5 digits."
                )
            if Driver.objects.filter(
                    license_number=license_number
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("A driver's license with "
                                            "this number already exists.")
        return license_number
