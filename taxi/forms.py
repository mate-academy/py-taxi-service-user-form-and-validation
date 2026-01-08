from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


def license_validate(license_number):
    if not (
        len(license_number) == 8
        and license_number[:3].isalpha()
        and license_number[:3].isupper()
        and license_number[3:].isnumeric()
    ):
        raise forms.ValidationError(
            "License number must be in the format XYZ12345"
        )
    return license_number


class DriverCreateForm(UserCreationForm):
    email_address = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "email_address",
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        return license_validate(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "license_number",
        )

    def clean_license_number(self):
        return license_validate(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = (
            "model",
            "manufacturer",
            "drivers",
        )
