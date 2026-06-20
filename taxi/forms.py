from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseNumberValidationMixin:
    LICENSE_NUMBER_LENGTH = 8

    def clean_license_number(self):
        license_number: str = self.cleaned_data["license_number"]
        if len(license_number) != self.LICENSE_NUMBER_LENGTH:
            raise forms.ValidationError(
                "License number must consist only of "
                f"{self.LICENSE_NUMBER_LENGTH} characters."
            )
        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise forms.ValidationError(
                "License number's first 3 characters "
                "must consist only of uppercase letters."
            )
        if not license_number[-5:].isdigit():
            raise forms.ValidationError(
                "License number's last 5 characters "
                "must consist only of digits."
            )
        return license_number


class DriverForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=get_user_model().objects.all(),
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers",)
