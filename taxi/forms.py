from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from taxi.models import Car


Driver = get_user_model()


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not license_number:
            return license_number

        if len(license_number) != 8:
            raise ValidationError("License number must be 8 characters long")

        if (
                not license_number[:3].isalpha()
                or not license_number[:3].isupper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits")

        return license_number


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarUpdateDriversListForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ()
