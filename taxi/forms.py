from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        return validate_license_number(license_number)


def validate_license_number(license_number):
    chars_length = 8

    if not license_number:
        raise ValidationError(
            "Field license_number cannot be empty"
        )

    if len(license_number) != chars_length:
        raise ValidationError(
            f"Ensure that license number length = {chars_length}"
        )

    first_three_chars = license_number[:3]

    if not first_three_chars.isalpha() or not first_three_chars.isupper():
        raise ValidationError(
            "First three characters must be uppercase letters"
        )

    last_five_chars = license_number[-5:]

    if not last_five_chars.isdigit():
        raise ValidationError(
            "Last five characters must be digits"
        )

    return license_number
