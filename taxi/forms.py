from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from taxi.models import Driver, Car


class LicenseNumberValidationMixin:

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (
                len(license_number) == 8
                and license_number[:3].isupper()
                and license_number[:3].isalpha()
                and license_number[-5:].isdigit()
        ):
            return license_number

        raise ValidationError(
            "Ensure that licence number "
            "consist only of 8 characters, "
            "first 3 characters are uppercase letters and "
            "last 5 characters are digits"
        )


class DriverForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
