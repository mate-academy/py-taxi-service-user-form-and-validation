from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    MAX_LENGTH = 8

    license_number = forms.CharField(max_length=MAX_LENGTH, required=True)

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise (ValidationError
                   ("License number must be exactly 8 characters long"))
        elif not (
                license_number[:3].isupper() and license_number[:3].isalpha()):
            raise ValidationError("First 3 symbols should be in uppercase")
        elif not license_number[-5:].isdigit():
            raise ValidationError("Last 5 symbols should be digit")
        return license_number
