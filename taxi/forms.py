from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from taxi.models import Driver, Car


class CarCreationForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not RegexValidator(
            regex=r"^[A-Z]{3}\d{5}$",
            message="Must be exactly 3 uppercase letters"
                    " followed by 5 digits (e.g., ABC12345).",
        )(license_number):
            raise forms.ValidationError("Invalid license number format.")
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
            "email",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not RegexValidator(
            regex=r"^[A-Z]{3}\d{5}$",
            message="Must be exactly 3 uppercase letters"
                    " followed by 5 digits (e.g., ABC12345).",
        )(license_number):
            raise forms.ValidationError("Invalid license number format.")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]
