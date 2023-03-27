from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "email",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    DRIVER_LICENSE_LEN = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    @staticmethod
    def check_upper(sequence: str) -> bool:
        return sequence == sequence.upper()

    @staticmethod
    def check_alpha(sequence: list) -> bool:
        return all([elem.isalpha() for elem in sequence])

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        license_number_start = license_number[0:3]

        if len(license_number) != self.DRIVER_LICENSE_LEN:
            raise ValidationError("license number must contain 8 characters.")
        if not (
            self.check_alpha(license_number_start)
            and self.check_upper(license_number_start)
        ):
            raise ValidationError("first 3 characters must be capital letters")

        if not "".join(license_number[3:]).isdigit():
            raise ValidationError("last 5 characters must be digits")
        return license_number


# class CarCreateForm(forms.ModelForm):
#     drivers = forms.ModelMultipleChoiceField(
#         queryset=get_user_model.
#     )
