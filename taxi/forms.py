from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverLicenseValidatorMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (
            len(license_number) != 8
            or not license_number[:3].isalpha()
            or not license_number[:3].isupper()
            or not license_number[3:8].isdigit()
        ):
            raise ValidationError("Incorrect license number")

        return license_number


class DriverLicenseUpdateForm(DriverLicenseValidatorMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class DriverCreationForm(DriverLicenseValidatorMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            UserCreationForm.Meta.fields
            + ("first_name", "last_name", "license_number", )
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
