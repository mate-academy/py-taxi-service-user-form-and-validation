from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.Form):
    license_number = forms.CharField()

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must consist of exactly 8 characters."
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "License number last 5 characters must be digits."
            )
        if not license_number[:3].isupper():
            raise forms.ValidationError(
                "License number first 3 characters should be upper case."
            )
        if not license_number[:3].isalpha():
            raise forms.ValidationError(
                "License number first 3 characters should be letters."
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
