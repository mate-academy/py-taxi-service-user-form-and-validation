from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class LicenseNumberValidationMixin(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError("License number must be 8 characters long.")

        if (
                not license_number[:3].isalpha()
                or not license_number[:3].isupper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits.")

        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            UserCreationForm.Meta.fields
            + ("first_name", "last_name", "license_number")
        )
        help_texts = {
            "license_number":
                "<ul><li>License number must be 8 characters long.</li>"
                "<li>First 3 characters must be uppercase letters.</li>"
                "<li>Last 5 characters must be digits</li></ul>"
        }


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)
        help_texts = {
            "license_number":
                "<ul><li>License number must be 8 characters long.</li>"
                "<li>First 3 characters must be uppercase letters.</li>"
                "<li>Last 5 characters must be digits</li></ul>"
        }


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
