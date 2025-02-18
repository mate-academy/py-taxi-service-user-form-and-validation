from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


def _validate_license_number(license_number: str) -> str:

    if len(license_number) != 8:
        raise ValidationError(
            "License number must be 8 characters long."
        )

    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "The first three symbols must be uppercase letters"
        )

    if not license_number[3:8].isnumeric():
        raise ValidationError(
            "Last five symbols must be digits"
        )

    return license_number


class DriverCreateForm(UserCreationForm):
    REQUIRED_NUMBER_OF_SYMBOLS = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        return _validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    REQUIRED_NUMBER_OF_SYMBOLS = 8

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        return _validate_license_number(license_number)


class CarForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"

# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError
#
#
# from taxi.models import Driver
#
#
# def _validate_license_number(license_number: str) -> str:
#     if len(license_number) != 8:
#         raise ValidationError("License number must have len()==8")
#     if not license_number[:3].isupper() or not license_number[:3].isalpha():
#         raise ValidationError("The first 3 digits must be uppercase()")
#     if not license_number[3:].isdigit():
#         raise ValidationError("The last 5 chars must be digits")
#     return license_number
#
#
# class DriverCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Driver
#         fields = UserCreationForm.Meta.fields + ("license_number",)
#
# class DriverLicenseUpdateForm(forms.ModelForm):
#
#     def clean_license_number(self):
#         license_number = self.cleaned_data["license_number"]
#         if len(license_number) > 8:
#             raise ValidationError("License number is too long")
#         if not license_number[:3].isuppper():
#             raise ValidationError("The first 3 digits must be uppercase")
#         if not license_number[3:].isdigit():
#             raise ValidationError("The last 5 chars must be digits")
#         return license_number
#
#     class Meta:
#         model = Driver
#         fields = ["license_number",]
