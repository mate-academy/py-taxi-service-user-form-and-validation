from django import forms

from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseNumberValidationMixin(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License must consist of 8 characters."
            )

        first_three = license_number[:3]
        last_five = license_number[3:]

        if not first_three.isupper() or not first_three.isalpha():
            raise forms.ValidationError(
                "The first 3 characters must be uppercase letters."
            )

        if not last_five.isdigit():
            raise forms.ValidationError(
                "The last 5 characters must be digits."
            )

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberValidationMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin):
    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
