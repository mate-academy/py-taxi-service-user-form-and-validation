from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CleanLicenseNumberMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        len_license_number = len(license_number)
        first_3 = license_number[:3]
        first_3_chars_alpha = first_3.isalpha()
        first_3_chars_uppercase = first_3 == first_3.upper()
        last_5 = license_number[-5:]
        last_5_is_digit = last_5.isdigit()

        if len_license_number != 8:
            raise ValidationError(
                f"Length of license number should be 8 symbols, not: "
                f"{len_license_number}"
            )
        if not first_3_chars_alpha or not first_3_chars_uppercase:
            raise ValidationError(
                f"The first 3 symbols should be uppercase letters, not: "
                f"{first_3}"
            )
        if not last_5_is_digit:
            raise ValidationError(
                f"The last 5 symbols should be digits, not: "
                f"{last_5}"
            )

        return self.cleaned_data["license_number"]


class DriverForm(forms.ModelForm, CleanLicenseNumberMixin):
    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password"
        )
        password = forms.CharField(
            label="Password",
            widget=forms.PasswordInput
        )

    def save(self, commit=True):
        driver = super().save(commit=False)
        driver.set_password(self.cleaned_data["password"])

        if commit:
            driver.save()

        return driver


class DriverLicenseUpdateForm(forms.ModelForm, CleanLicenseNumberMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = (
            "model",
            "manufacturer",
            "drivers"
        )
