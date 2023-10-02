from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import MaxValueValidator

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must contain 8 characters"
            )

        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise forms.ValidationError(
                "License number must start with 3 uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "License number must end with 5 digits"
            )

        return license_number


class DriverCreationForm(DriverLicenseUpdateForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
