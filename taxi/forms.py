from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Should be consist only of 8 characters")

        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise ValidationError("First 3 characters are uppercase letters")

        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 characters are digits")

        return license_number


class DriverCreateForm(LicenseValidationMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "license_number",
        )


class BaseCarForm(forms.ModelForm):
    drivers = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
