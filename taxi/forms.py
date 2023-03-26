from __future__ import annotations
from string import ascii_uppercase

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverForm(UserCreationForm):
    license_number = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    MIN_MAX_LEN = 8

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if (
            len(license_number) != self.MIN_MAX_LEN
            or len(
                [
                    symbol
                    for symbol in license_number[:3]
                    if symbol in ascii_uppercase
                ]
            )
            != len(license_number[:3].upper())
            or not license_number[-1:-6:-1].isdigit()
        ):
            raise forms.ValidationError("Provide proper license number")
        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
