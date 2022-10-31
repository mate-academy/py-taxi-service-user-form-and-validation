from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    UPPERCASE_CHARS_NUM = 3
    DIGIT_CHARS_NUM = 5
    LICENSE_NUMBER_LENGTH = UPPERCASE_CHARS_NUM + DIGIT_CHARS_NUM

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_NUMBER_LENGTH:
            raise ValidationError(
                f"License number must consist of "
                f"{self.LICENSE_NUMBER_LENGTH} characters!"
            )

        if not (
            license_number[: self.UPPERCASE_CHARS_NUM].isalpha()
            and license_number[: self.UPPERCASE_CHARS_NUM].isupper()
        ):
            raise ValidationError(
                f"First {self.UPPERCASE_CHARS_NUM} "
                f"characters must be uppercase letters!"
            )

        if not license_number[self.UPPERCASE_CHARS_NUM :].isdigit():
            raise ValidationError(
                f"Last {self.DIGIT_CHARS_NUM} characters must be digits!"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
