from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


User = get_user_model()


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters long"
            )
        first_three = license_number[:3]
        last_five = license_number[3:]
        if not all(ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for ch in first_three):
            raise forms.ValidationError(
                "First three characters must be uppercase A–Z"
            )
        if not all(ch in "0123456789" for ch in last_five):
            raise forms.ValidationError(
                "Last five characters must be digits 0–9"
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters long"
            )
        first_three = license_number[:3]
        last_five = license_number[3:]
        if not all(ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for ch in first_three):
            raise forms.ValidationError(
                "First three characters must be uppercase A–Z"
            )
        if not all(ch in "0123456789" for ch in last_five):
            raise forms.ValidationError(
                "Last five characters must be digits 0–9"
            )
        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
