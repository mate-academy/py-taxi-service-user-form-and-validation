from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_license_number(value):
    if len(value) != 8:
        raise forms.ValidationError(
            "License number must consist of exactly 8 characters."
        )
    if not value[:3].isupper() or not value[:3].isalpha():
        raise forms.ValidationError(
            "First 3 characters must be uppercase letters."
        )
    if not value[3:].isdigit():
        raise forms.ValidationError(
            "Last 5 characters must be digits."
        )
    return value


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(
            self.cleaned_data["license_number"]
        )
