from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not (
                len(license_number) == 8
                and (license_number[:3].isupper()
                     and license_number[:3].isalpha())
                and license_number[3:].isdigit()
        ):
            raise ValidationError(
                "Enter a valid license_number",
            )
        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
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
