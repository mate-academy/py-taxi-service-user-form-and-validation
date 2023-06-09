from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator, MinLengthValidator

# from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


# class DriverCreationForm(UserCreationForm):
#     LICENSE_LENGTH = 8
#     FIRST_CHARACTERS_TO_BE_UPPER = 3
#     LAST_CHARACTERS_TO_BE_DIGIT = 5
#
#     # def clean_license_number(self):
#     #     license_number = self.cleaned_data["license_number"]
#     #     if len(license_number) != DriverCreationForm.LICENSE_LENGTH:
#     #         raise ValidationError(
#                 f"The license number must be " \
#                 f"{DriverCreationForm.LICENSE_LENGTH} characters long"
#     #         )
#     #     elif not license_number[
#     #              :DriverCreationForm.FIRST_CHARACTERS_TO_BE_UPPER
#     #              ].isupper():
#     #         raise ValidationError(
#     #             f"The first {DriverCreationForm.FIRST_CHARACTERS_TO_BE_UPPER} "
#     #             f"characters of license number must be uppercase"
#     #         )
#     #     elif not license_number[
#     #              -DriverCreationForm.LAST_CHARACTERS_TO_BE_DIGIT:
#     #              ].isdigit():
#     #         raise ValidationError(
#     #             f"The last {DriverCreationForm.LAST_CHARACTERS_TO_BE_DIGIT} "
#     #             f"characters of license number must be digits"
#     #         )
#     #     return license_number
#
#     class Meta(UserCreationForm.Meta):
#         model = Driver
#         fields = UserCreationForm.Meta.fields + (
#             "first_name",
#             "last_name",
#             "license_number",
#         )

class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    # uppercase_validator = RegexValidator(
    #     regex=r"^[A-Z]{3}",
    #     message="First 3 letters must be uppercase."
    # )
    # length_validator = RegexValidator(
    #     r'^.{8}$', message="License number must be 8 characters long."
    # )
    # digits_validator = RegexValidator(
    #     regex=r"\d{5}$",
    #     message="Last 5 characters must be digits."
    # )
    # license_number = forms.CharField(
    #     required=True,
    #     validators=[uppercase_validator, length_validator, digits_validator]
    # )

    class Meta:
        model = Driver
        fields = ("license_number",)
