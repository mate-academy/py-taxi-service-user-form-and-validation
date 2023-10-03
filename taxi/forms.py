from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Driver, Car


class LicenseNumberMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must consist of 8 characters"
            )
        if not license_number[:3].isupper():
            raise forms.ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError("Last 5 characters must be digits")
        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberMixin):
    license_number = forms.CharField(max_length=8, required=True)

    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name", "email",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberMixin):
    license_number = forms.CharField(max_length=8, required=True)

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Car
        fields = "__all__"
