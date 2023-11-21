from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from .models import Driver, Car


class LicenseNumberValidationMixin(forms.ModelForm):
    LENGTH = 8
    FIRST_PART = 3

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LENGTH:
            raise ValidationError(
                f"The length of the license number must be {self.LENGTH}"
            )
        if (
            not license_number[:self.FIRST_PART].isupper()
            or not license_number[:self.FIRST_PART].isalpha()
        ):
            raise ValidationError(
                f"The first {self.FIRST_PART} characters "
                f"must be uppercase letters."
            )
        if not license_number[self.FIRST_PART:].isdigit():
            raise ValidationError(f"Last {self.LENGTH - self.FIRST_PART}"
                                  f" characters must be digit numbers")
        return license_number


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (UserCreationForm.Meta.fields +
                  ("first_name", "last_name", "license_number", ))


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
