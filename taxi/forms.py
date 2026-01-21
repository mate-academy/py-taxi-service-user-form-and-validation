from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Car


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("license_number should be equal to 8")
        elif not (
                license_number[:3].isalpha() and license_number[:2].isupper()
        ):
            raise ValidationError(
                "license_number should " "start with uppercase letter"
            )
        elif not license_number[3:].isnumeric():
            raise ValidationError(
                "license_number should " "ending with numeric characters"
            )
        return license_number


class DriverCreatingForm(LicenseValidationMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]


class CarCreatingForm(LicenseValidationMixin, forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
