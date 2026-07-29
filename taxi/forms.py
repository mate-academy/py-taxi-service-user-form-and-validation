from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Car

Driver = get_user_model()

license_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License number must consist of 3 uppercase letters and 5 digits.",
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[license_validator]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if Driver.objects.filter(license_number=license_number).exists():
            raise forms.ValidationError(
                "A driver with this license number already exists."
            )

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[license_validator]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if Driver.objects.filter(
            license_number=license_number
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "A driver with this license number already exists."
            )

        return license_number


class CarCreationForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
