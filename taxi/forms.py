from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


from taxi.models import Driver, Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError(f"Licence number length must be 8 characters.")
    if not (license_number[:3].isalpha() and license_number[:3].isupper()):
        raise ValidationError(f"First 3 characters must be upper-case letters")
    if not license_number[3:].isdigit():
        raise ValidationError(f"Last 5 characters must be digits")
    return license_number

class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number



class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Drivers"
    )
    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
