from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validation_license_number(license_number):

    if len(license_number) != 8:
        raise ValidationError("Must consist only of 8 characters")
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters")
    if not license_number[-5].isdigit():
        raise ValidationError("Last 5 characters must be digits")

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
