from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.Form):
    license_number = forms.CharField(max_length=8)

    def clean_license_number(self):
        error = forms.ValidationError("License number not valid")
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != 8:
            raise error
        for char in license_number[:3]:
            if char.isnumeric():
                raise error
        if license_number[:3] != license_number[:3].upper():
            raise error
        if not license_number[3:].isdigit():
            raise error
        return license_number


class DriverForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )

    def clean_license_number(self):
        error = forms.ValidationError("License number not valid")
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != 8:
            raise error
        for char in license_number[:3]:
            if char.isnumeric():
                raise error
        if license_number[:3] != license_number[:3].upper():
            raise error
        if not license_number[3:].isdigit():
            raise error
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
