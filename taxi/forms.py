from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class LicenseNumberValidationForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "The license must contain 8 characters"
            )
        if (not license_number[:3].isalpha()) \
                or (not license_number[:3].isupper()):
            raise ValidationError(
                "The first three characters must be uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "The last five characters must be numbers"
            )

        return license_number


class DriverCreationForm(LicenseNumberValidationForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )


class DriverLicenseUpdateForm(LicenseNumberValidationForm, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
