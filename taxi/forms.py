from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=8)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password1",
            "password2",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters"
            )

        if not (
            license_number[:3].isalpha()
            and license_number[:3].isupper()
            and license_number[3:].isdigit()
        ):
            raise forms.ValidationError(
                "License number must be 3 uppercase letters and 5 digits"
            )

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters"
            )

        if not (
            license_number[:3].isalpha()
            and license_number[:3].isupper()
            and license_number[3:].isdigit()
        ):
            raise forms.ValidationError(
                "License number must be 3 uppercase letters and 5 digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
