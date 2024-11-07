from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm
)
from taxi.models import (
    Driver,
    Car
)

CHAR_AMOUNT = 8


class Validator:
    def __init__(self):
        self.cleaned_data = None

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != CHAR_AMOUNT:
            raise forms.ValidationError(
                f"Invalid length of license number ({CHAR_AMOUNT})"
            )
        elif (not license_number[:3].isalpha()
              or not license_number[:3].isupper()):
            raise forms.ValidationError(
                "Invalid license number."
                "First 3 characters should be uppercase letters"
            )
        elif not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Invalid license number. Last 5 characters should be digits"
            )
        return license_number


class DriverCreationForm(UserCreationForm, Validator):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(UserChangeForm, Validator):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
