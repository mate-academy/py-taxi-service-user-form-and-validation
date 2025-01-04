from django import forms
from .models import Driver, Car
import re
from django.contrib.auth.forms import UserCreationForm


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "license_number must have 8 characters")

        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "license_number must begin with 3 "
                "Uppercase letters and then 5 digits"
            )

        return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=255)

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "license_number must have 8 characters")

        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "license_number must begin with 3 "
                "Uppercase letters and then 5 digits"
            )

        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
