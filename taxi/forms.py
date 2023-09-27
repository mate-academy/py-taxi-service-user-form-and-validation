from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenceNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        license_number_first_3_letters = license_number[:3]

        if len(license_number) != 8:
            raise ValidationError("License number must contains 8 characters")

        if (
            not license_number_first_3_letters.isalpha()
            or license_number_first_3_letters
            != license_number_first_3_letters.upper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )

        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 character must be digits")

        return license_number


class DriverCreateForm(UserCreationForm, LicenceNumberValidationMixin):
    class Meta:
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("license_number", "first_name", "last_name", "email"))


class DriverLicenseUpdateForm(forms.ModelForm, LicenceNumberValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
