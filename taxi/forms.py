from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "The license number must be exactly 8 characters long."
            )
        alpha_part = license_number[:3]
        digits_part = license_number[3:]
        if not (alpha_part.isalpha() and alpha_part.isupper()):
            raise forms.ValidationError(
                "First 3 characters must be uppercase letters."
            )
        if not digits_part.isdigit():
            raise forms.ValidationError(
                "Last 5 characters must be digits"
            )
        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
