from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from taxi.models import Car


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_value = self.cleaned_data["license_number"]
        errors = []
        if len(license_value) != 8:
            errors.append("License number should consist only of 8 characters")
        if (not license_value[:3].isalpha()
                or license_value[:3] != license_value[:3].upper()):
            errors.append("First 3 characters should be uppercase letters")
        if not license_value[3:].isnumeric():
            errors.append("Last 5 characters should be digits")

        if errors:
            raise ValidationError(errors)
        return license_value


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]


class CarCreateForm(ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
