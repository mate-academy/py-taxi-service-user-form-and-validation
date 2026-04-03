from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    MIN_LENGTH = 8

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.MIN_LENGTH:
            raise forms.ValidationError(
                "license_number must contain only "
                f"{DriverLicenseUpdateForm.MIN_LENGTH} characters"
            )

        if (
            not license_number[:3].isalpha()
            or not license_number[:3].isupper()
        ):
            raise forms.ValidationError(
                "license_number first 3 characters are uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "license_number last 5 characters are digits"
            )

        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
