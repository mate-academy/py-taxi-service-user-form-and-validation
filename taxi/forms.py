from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model

from taxi.models import Car, Driver


class LicenseNumberValidatorMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number", "")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters long"
            )

        prefix, suffix = license_number[:3], license_number[3:]

        if not (prefix.isalpha() and prefix.isupper()):
            raise forms.ValidationError(
                "License number prefix must be three uppercase letters"
            )

        if not suffix.isdigit():
            raise forms.ValidationError(
                "License number suffix must be numeric"
            )

        return license_number


class DriverLicenseUpdateForm(LicenseNumberValidatorMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(LicenseNumberValidatorMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = (
            "model",
            "manufacturer",
            "drivers",
        )
