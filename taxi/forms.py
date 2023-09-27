from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class CleanLicenseNumberMixine():
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number should be 8 characters long."
            )
        first_three = license_number[0:3]
        if not first_three.isupper() or not first_three.isalpha():
            raise forms.ValidationError(
                "The first three characters should be uppercase letters."
            )
        if not license_number[-5:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters should be digits."
            )
        return license_number


class DriverCreationForm(UserCreationForm, CleanLicenseNumberMixine):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm, CleanLicenseNumberMixine):
    class Meta:
        model = Driver
        fields = (
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = (
            "model",
            "manufacturer",
            "drivers",
        )
