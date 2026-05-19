from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberValidationMixin(forms.ModelForm):
    LENGTH = 8
    FIRST_LETTERS = 3
    LAST_DIGITS = 5

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LENGTH:
            raise ValidationError("Incorrect LicenseNumber")

        first_part = license_number[:self.FIRST_LETTERS]
        if not (first_part.isalpha() and first_part.isupper()):
            raise ValidationError("Incorrect LicenseNumber")

        if not license_number[-self.LAST_DIGITS:].isdigit():
            raise ValidationError("Incorrect LicenseNumber")

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberValidationMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
