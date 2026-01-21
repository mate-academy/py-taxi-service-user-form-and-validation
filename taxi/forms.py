import re

from django import forms

from taxi.models import Driver, Car

from django.contrib.auth.forms import UserCreationForm


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}\d{5}$"
        if not re.match(pattern, license_number):
            raise forms.ValidationError(
                "License number must consist of 3 uppercase"
                " letters followed by 5 digits (e.g. ABC12345)."
            )
        return license_number


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        pattern = r"^[A-Z]{3}\d{5}$"
        if not re.match(pattern, license_number):
            raise forms.ValidationError(
                "License number must consist of 3 uppercase"
                " letters followed by 5 digits (e.g. ABC12345)."
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
