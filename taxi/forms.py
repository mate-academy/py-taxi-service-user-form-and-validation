from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        def first_3_uppercase_letters():
            first_3_letters = license_number[:3]

            if not first_3_letters.isupper():
                return False

            if not first_3_letters.isalpha():
                return False

            return True

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters long"
            )
        if not first_3_uppercase_letters():
            raise forms.ValidationError(
                "License number must start with 3 uppercase letters"
            )
        if not license_number[-5:].isdigit():
            raise forms.ValidationError(
                "License number must end with 5 digits"
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreateForm(UserCreationForm, LicenseNumberValidationMixin):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "email", "license_number",
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
