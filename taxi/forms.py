from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class DriverLicenseCreateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError("Invalid license number")
        if not license_number[:3].isalpha():
            raise forms.ValidationError("Error")
        if not license_number[:3].isupper():
            raise forms.ValidationError("Error")
        if not license_number[3:].isdigit():
            raise forms.ValidationError("Invalid license number")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError("Invalid license number")
        if not license_number[:3].isalpha():
            raise forms.ValidationError("Error")
        if not license_number[:3].isupper():
            raise forms.ValidationError("Error")
        if not license_number[3:].isdigit():
            raise forms.ValidationError("Invalid license number")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
