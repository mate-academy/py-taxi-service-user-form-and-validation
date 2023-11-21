from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


def clean_license_number_form(license_number):
    if len(license_number) != 8:
        raise ValidationError("lengths must be 8")
    elif not (license_number[:3].isalpha() and license_number[:3].isupper()):
        raise ValidationError("first 3 letters must be upper and A-Z")
    elif not (license_number[3:].isdigit()):
        raise ValidationError("must be 5 numbers")
    return license_number


class DriverCreationForms(UserCreationForm):
    class Meta(UserCreationForm):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number",)

        def clean_license_number(self):
            license_number = self.cleaned_data["license_number"]
            return clean_license_number_form(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return clean_license_number_form(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
