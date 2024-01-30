from django import forms
from django.core.exceptions import ValidationError

from .models import Driver


# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm


# class AbstractUserFormIfCustom(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Driver
#         fields = UserCreationForm.Meta.fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    model = Driver

    class Meta:
        model = Driver
        fields = ('license_number',)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        license_number_len_required = 8
        first_3_characters = license_number[:3:]
        last_5_characters = license_number[3::]

        validation_error_message = "Ensure the license_number:\n"

        if len(license_number) != license_number_len_required:
            validation_error_message += "- Consists only of 8 characters\n"

        if not first_3_characters.isalpha() or not first_3_characters.isupper():
            validation_error_message += "- First 3 characters are uppercase letters\n"

        if not last_5_characters.isnumeric():
            validation_error_message += "- Last 5 characters are digits"

        if len(validation_error_message) > len("Ensure the license_number:\n"):
            raise ValidationError(validation_error_message)

        return license_number
