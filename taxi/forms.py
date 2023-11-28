from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validation_license_number(license_number):
    length = 8
    first_char = 3
    last_char = 5

    if len(license_number) != length:
        raise ValidationError(f"Must consist only of {length} characters")
    if not license_number[:first_char].isalpha() or \
            not license_number[:first_char].isupper():
        raise ValidationError(
            f"First {first_char} characters must be uppercase letters"
        )
    if not license_number[-last_char].isdigit():
        raise ValidationError(f"Last {last_char} characters must be digits")

    return license_number


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("license_number", "first_name", "last_name", )
                  )

    def clean_license_number(self):
        return validation_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    def clean_license_number(self):
        return validation_license_number(self.cleaned_data["license_number"])

    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
