from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car
from django.contrib.auth.forms import UserCreationForm


def _clean_license_number(cleaned_data: dict) -> None:
    length = 8
    first_upper_letters = 3
    last_digits = 5

    license_number = cleaned_data["license_number"]

    if len(license_number) != length:
        raise ValidationError(f"Length must be {length}")
    if (not license_number[:first_upper_letters].isalpha()
            or not license_number[:first_upper_letters].isupper()):
        raise ValidationError(f"First {first_upper_letters} chars "
                              "must be upper-case letters")
    if not license_number[-last_digits:].isdigit():
        raise ValidationError(f"Last {last_digits} chars must be digits")


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("username", "license_number", "first_name", "last_name", "email",)

    def clean(self):
        _clean_license_number(cleaned_data=self.cleaned_data)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean(self):
        _clean_license_number(cleaned_data=self.cleaned_data)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
