from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverLicenseValidationMixin(forms.ModelForm):
    LICENSE_LENGTH = 8
    LICENSE_CHARACTERS = 3
    LICENSE_DIGITS = 5

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError("License number must contain 8 characters")
        if (not license_number[:self.LICENSE_CHARACTERS].isupper()
                or not license_number[:self.LICENSE_CHARACTERS].isalpha()):
            raise ValidationError(
                "First 3 characters of your driver license"
                " must be uppercase letters"
            )
        if not license_number[-self.LICENSE_DIGITS:].isdigit():
            raise ValidationError(
                "Last 5 characters of your driver license must be digits"
            )
        return license_number


class DriverCreateForm(DriverLicenseValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(DriverLicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
