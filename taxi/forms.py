from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


def validate_license_number(license_number: str) -> str:
    if not len(license_number) == 8:
        raise ValidationError("Driver license has to consist of 8 characters.")

    if not (license_number[:3].isupper() and license_number[:3].isalpha()):
        raise ValidationError("Incorrect license code.")

    if not license_number[3:].isdigit():
        raise ValidationError("Incorrect license number.")

    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data.get("license_number")

        return validate_license_number(license_number)


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Car
        fields = "__all__"
