from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Car


class LicenseNumberValidatorMixin:
    LICENSE_LENGTH = 8
    UPPER_COUNT = 3
    DIGITS_COUNT = 5

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError(
                f"License number may consist only of "
                f"{self.LICENSE_LENGTH} characters."
            )

        if (
            not license_number[:self.UPPER_COUNT].isupper()
            or not license_number[:self.UPPER_COUNT].isalpha()
        ):
            raise ValidationError(
                f"First {self.UPPER_COUNT} characters of license number "
                f"should be uppercase letters."
            )

        if not license_number[-self.DIGITS_COUNT:].isdigit():
            raise ValidationError(
                f"Last {self.DIGITS_COUNT} characters of license number "
                f"should be digits."
            )

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberValidatorMixin):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberValidatorMixin):
    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
