from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Driver


def validate_license_number(license_number):
    return (
        len(license_number) == 8
        and license_number[:3].isalpha()
        and license_number[:3].isupper()
        and license_number[3:].isdigit()
    )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not license_number:
            raise forms.ValidationError("License number is required.")
        if not validate_license_number(license_number):
            raise forms.ValidationError("License number is invalid.")
        return license_number


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(max_length=8, required=True, min_length=1)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not validate_license_number(license_number):
            raise forms.ValidationError("License number is invalid.")
        return license_number
