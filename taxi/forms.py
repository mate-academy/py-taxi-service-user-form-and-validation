from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


from taxi.models import Driver


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("license number must be 8 characters long")

        if not license_number[:3].isalpha()\
                or not license_number[:3].isupper():
            raise ValidationError(
                "the first three characters must be uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError("the last five characters must be digits")

        return license_number


class DriverCreateFrom(UserCreationForm, DriverLicenseUpdateForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )
